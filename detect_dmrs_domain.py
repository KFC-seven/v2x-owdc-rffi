# detect_dmrs_domain.py
# 直接运行输出判断结果：
#   python detect_dmrs_domain.py
# 或者指定数据目录：
#   python detect_dmrs_domain.py --mat_dir "E:/rf_datasets_IQ_raw"

import os
import glob
import argparse
import numpy as np
import h5py
from collections import Counter


def papr_db(x: np.ndarray) -> float:
    p = np.abs(x) ** 2
    p_mean = float(np.mean(p) + 1e-12)
    p_peak = float(np.max(p) + 1e-12)
    return 10.0 * np.log10(p_peak / p_mean)


def candidate_nffts(L: int):
    # 常见 LTE/OFDM FFT sizes（你这里 1.4MHz 很常见的是 128）
    cands = [64, 128, 256, 512, 1024, 2048]
    return [c for c in cands if c < L]


def cp_corr_score(x: np.ndarray, nfft: int, cp_len: int) -> float:
    # x = [CP | symbol] 时，x[:cp] 与 x[nfft:nfft+cp] 相关性会高
    if cp_len <= 0 or nfft + cp_len > len(x):
        return 0.0
    a = x[:cp_len]
    b = x[nfft:nfft + cp_len]
    na = np.linalg.norm(a) + 1e-12
    nb = np.linalg.norm(b) + 1e-12
    return float(np.abs(np.vdot(a, b)) / (na * nb))


def classify_one_sequence(x: np.ndarray):
    L = len(x)
    mag = np.abs(x)
    mag_mean = float(np.mean(mag) + 1e-12)
    mag_std = float(np.std(mag))
    mag_cv = mag_std / mag_mean  # |x| 变异系数：频域常模序列通常更小
    p = papr_db(x)

    # 频域（占用子载波）最直观特征：6RB -> 72 子载波
    # 因此 L=72 或 72 的倍数（<=576）非常像频域映射
    length_like_freq = (L == 72) or (L % 72 == 0 and L <= 576)

    # 常模倾向：DMRS/QPSK/ZC 在“频域子载波符号”层面通常 |x| 接近常数
    const_modulus_like = (mag_cv < 0.15)  # 经验阈值，可按数据微调

    # CP 检测：尝试不同 nfft，找最可能的 (nfft, cp_len=L-nfft)
    best_cp = (0.0, None, None)  # (score, nfft, cp_len)
    for nfft in candidate_nffts(L):
        cp_len = L - nfft
        # CP 长度一般在 3%~25% nfft（过大/过小都不合理）
        if not (0.03 * nfft <= cp_len <= 0.25 * nfft):
            continue
        score = cp_corr_score(x, nfft=nfft, cp_len=cp_len)
        if score > best_cp[0]:
            best_cp = (score, nfft, cp_len)

    cp_score, cp_nfft, cp_len = best_cp
    has_cp = cp_score > 0.35  # 越大越保守
    high_papr = p > 6.0       # 时域 OFDM 常见较高 PAPR（启发式）

    evidence = {
        "L": L,
        "mag_cv": mag_cv,
        "papr_db": p,
        "length_like_freq": length_like_freq,
        "const_modulus_like": const_modulus_like,
        "best_cp_score": cp_score,
        "best_cp_nfft": cp_nfft,
        "best_cp_len": cp_len
    }

    if has_cp and high_papr:
        return "TIME_CP", evidence
    if length_like_freq and const_modulus_like and (p < 3.0):
        return "FREQ", evidence
    if high_papr and not has_cp:
        return "TIME_NOCP", evidence
    if length_like_freq and (p < 5.0):
        return "FREQ?", evidence
    return "UNCERTAIN", evidence


def load_dmrs_from_mat(mat_path: str):
    """
    兼容你给的读取方式：
      rfDataset = f['rfDataset']
      dmrs_struct = rfDataset['dmrs'][:]
      dmrs_complex = dmrs_struct['real'] + 1j * dmrs_struct['imag']
    """
    with h5py.File(mat_path, "r") as f:
        rfDataset = f["rfDataset"]
        dmrs_struct = rfDataset["dmrs"][:]  # compound dtype array
        if ("real" not in dmrs_struct.dtype.names) or ("imag" not in dmrs_struct.dtype.names):
            raise KeyError(f"dmrs fields not found. dtype.names={dmrs_struct.dtype.names}")
        dmrs_complex = dmrs_struct["real"] + 1j * dmrs_struct["imag"]
    return dmrs_complex


def summarize_evidence(evidences):
    paprs = np.array([ev["papr_db"] for ev in evidences], dtype=float)
    cvs = np.array([ev["mag_cv"] for ev in evidences], dtype=float)
    cps = np.array([ev["best_cp_score"] for ev in evidences], dtype=float)
    return {
        "papr_median": float(np.median(paprs)),
        "papr_p90": float(np.quantile(paprs, 0.9)),
        "cv_median": float(np.median(cvs)),
        "cv_p90": float(np.quantile(cvs, 0.9)),
        "cp_median": float(np.median(cps)),
        "cp_p90": float(np.quantile(cps, 0.9)),
    }


def main(mat_dir: str, max_files: int = 10, max_records: int = 200):
    mat_files = sorted(glob.glob(os.path.join(mat_dir, "*.mat")))
    if len(mat_files) == 0:
        raise RuntimeError(f"No .mat found in: {mat_dir}")

    mat_files = mat_files[: min(len(mat_files), max_files)]
    print(f"[INFO] mat_dir = {mat_dir}")
    print(f"[INFO] Found {len(mat_files)} mat files (checking up to max_files={max_files}).")

    overall_counts = Counter()
    length_set = set()

    for fp in mat_files:
        try:
            dmrs_complex = load_dmrs_from_mat(fp)
        except Exception as e:
            print(f"[ERROR] {os.path.basename(fp)} load failed: {e}")
            continue

        N, L = dmrs_complex.shape
        length_set.add(L)
        n_take = min(N, max_records)

        labels = []
        evidences = []
        for i in range(n_take):
            x = dmrs_complex[i, :].astype(np.complex64)
            # 归一化（不改变 PAPR 形态），避免幅度差异影响统计
            x = x / (np.sqrt(np.mean(np.abs(x) ** 2)) + 1e-12)
            lab, ev = classify_one_sequence(x)
            labels.append(lab)
            evidences.append(ev)

        c = Counter(labels)
        overall_counts.update(c)
        stats = summarize_evidence(evidences)
        majority = c.most_common(1)[0][0]

        print("\n" + "=" * 86)
        print(f"[FILE] {os.path.basename(fp)}")
        print(f"  dmrs shape = {dmrs_complex.shape}  (N={N}, L={L})")
        print(f"  label counts (first {n_take} records): {dict(c)}")
        print(f"  PAPR(dB): median={stats['papr_median']:.2f}, p90={stats['papr_p90']:.2f}")
        print(f"  |x| CV : median={stats['cv_median']:.3f}, p90={stats['cv_p90']:.3f}")
        print(f"  CP corr: median={stats['cp_median']:.3f}, p90={stats['cp_p90']:.3f}")
        print(f"  ==> Majority guess: {majority}")

    print("\n" + "#" * 86)
    print("[SUMMARY]")
    print(f"  Unique lengths observed: {sorted(list(length_set))}")
    print(f"  Overall label counts: {dict(overall_counts)}")

    print("\n[INTERPRETATION]")
    print("  - 若 L 常见为 72/144/216/288 且 |x| CV 小、PAPR 低 => 更像频域子载波 DMRS。")
    print("  - 若 L 常见接近 NFFT+CP 且 CP corr(p90) 明显偏大、PAPR 高 => 更像时域 OFDM(含CP)。")
    print("  - 若 PAPR 高但 CP corr 不明显 => 可能是时域 OFDM(不含CP) 或被截取/加窗后的符号段。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mat_dir",
        type=str,
        default=r"E:/rf_datasets_IQ_raw",  # 你可以改这个默认路径
        help="包含 .mat 文件的文件夹（默认已写死，可用命令行覆盖）"
    )
    parser.add_argument("--max_files", type=int, default=72)
    parser.add_argument("--max_records", type=int, default=2000)
    args = parser.parse_args()

    main(mat_dir=args.mat_dir, max_files=args.max_files, max_records=args.max_records)