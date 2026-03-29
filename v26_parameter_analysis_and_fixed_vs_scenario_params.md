# v26.2 / v26.3 参数分析与“固定参数 / 场景参数”划分建议

## 一、参数分类命名建议

为了在论文中更清晰地表达参数作用，建议将参数分成两类：

### 1. 默认固化参数（default-stable parameters）
含义：在不同安全场景下通常都可以取一个固定默认值，不需要随着场景目标显著改变。它们的主要作用是提供稳定、可复现、可解释的基础工作点。

可选中文命名：
- 默认固化参数
- 基础设定参数
- 默认工作点参数

建议英文命名：
- **default-stable parameters**
- 或 **globally fixed parameters**

### 2. 场景调谐参数（scenario-sensitive parameters）
含义：这些参数会显著改变工作点，影响 `FAR_unknown_accept`、`FRR_stable`、`miss_drift_all`、`drift_acc_all` 之间的权衡，因此应根据不同应用场景（高安全、高识别、平衡型）选择不同取值。

可选中文命名：
- 场景调谐参数
- 场景敏感参数
- 工作点调节参数

建议英文命名：
- **scenario-sensitive parameters**
- 或 **operating-point parameters**

其中，如果论文里更强调“安全-连续性权衡”，推荐用 **operating-point parameters**，因为它更准确地体现“这些参数决定系统工作点”。

## 二、当前数据是否足以支撑“固定参数默认选择”章节

结论：**基本足够。**

当前已有的数据链条是完整的：
1. v23 单参数 sweep 已验证三大主参数的单独作用趋势；
2. `joint_small` 已给出小范围组合搜索结果；
3. v26.2 已对多种二级参数做过粗扫，说明还有哪些参数值得保留、哪些影响有限；
4. v26.3 已围绕 `joint_e` 做局部微调，并把新的局部最优点跑出来。

因此，目前已经可以支持一个“固定参数默认选择”章节，逻辑可以写成：
- 先通过单参数 sweep 确定主导参数；
- 再通过 joint search 确定主参数的合理中心；
- 再通过 secondary sweep 判断哪些次级参数值得纳入默认参数集考虑；
- 最后通过 local tuning 得到新的默认工作点。

## 三、固定参数与场景参数的推荐划分

### 1. 建议归入“默认固化参数”的参数
基于 v26.2 结果，以下参数更适合先固定默认值：

- `gamma_drift`
- `lambda_sup`
- `lambda_proto`
- `conf_smooth`
- `wmax`
- `unknown_energy_margin`
- `energy_bg_q`
- `energy_bg_ema`
- `sup_eval_thr`
- `unk_eval_thr`

其中最值得考虑纳入默认值优化的是：
- `wmax`
- `gamma_drift`
- `lambda_proto`

其余参数目前更像低敏感或次低敏感参数，可先固定在现值。

### 2. 建议归入“场景调谐参数”的参数
基于 v23 与 v26.3 的结果，以下参数最明显决定系统工作点：

- `lambda_unkE`
- `lambda_stab`
- `gamma_notunk`

它们直接控制：
- unknown-side 排斥强度
- stable 保护强度
- support 权重形状 / 覆盖率

因此建议后续把这 3 个参数作为“场景参数”继续搜索和推荐。

## 四、v26.2 的主要发现

### 1. `wmax`
是当前二级参数中最值得保留的参数。`wmax=1.25` 给出了很强的整体表现，说明限制权重上限过紧可能会抑制有效监督，而适度放宽更有利于 `drift_acc_all` 与 `FRR_stable` 的平衡。

### 2. `gamma_drift`
有一定影响，但更像“精细修形参数”。其中 `0.75` 左右表现较好，过大（如 1.5）开始变差。

### 3. `lambda_proto`
表现出“小一点通常更好”的趋势，`0.1` 优于默认 `0.25` 的现象值得进一步关注。

### 4. `energy_bg_q`
更像典型的场景参数：
- 大一些更偏安全拒识；
- 小一些更偏低误拒。

它不适合作为唯一全局最优参数，但适合在“不同场景参数推荐”章节中展开。

## 五、v26.3 的主要发现：新的平衡点如何找出来

v26.3 的搜索中心是旧的 `joint_e`：
- `gamma_notunk = 1.0`
- `lambda_unkE = 0.05`
- `lambda_stab = 0.02`

在此基础上，局部搜索了：
- `gamma_notunk ∈ {0.9, 1.0}`
- `lambda_unkE ∈ {0.045, 0.05, 0.055}`
- `lambda_stab ∈ {0.015, 0.02, 0.03}`

结果表明，新的整体平衡点落在：
- `gamma_notunk = 1.0`
- `lambda_unkE = 0.045`
- `lambda_stab = 0.02`

即：
**`gu1__lu0p045__ls0p02`**

这个点优于旧 base 的原因不是单一指标暴涨，而是：
- `drift_acc_all` 进一步提升；
- `FRR_stable` 显著下降；
- `FAR_unknown_accept` 虽有小幅回升，但仍在可接受范围；
- 整体呈现出更均衡的工作点。

因此，这个点可以作为新的“平衡型默认参数集”。

## 六、建议写入论文的参数选择逻辑

### 1. 默认固化参数的选择逻辑
可以这样写：

> 首先通过 secondary coarse sweep（v26.2）评估次级参数对整体性能的影响。结果表明，除 `wmax`、`gamma_drift`、`lambda_proto` 外，其余次级参数对核心指标的影响较小或不稳定。因此，在后续实验中将这些参数固定为默认值，以减少搜索空间并提高参数解释性。

### 2. 场景调谐参数的选择逻辑
可以这样写：

> 进一步分析发现，`lambda_unkE`、`lambda_stab` 与 `gamma_notunk` 是决定工作点的关键参数，它们显著影响 `FAR_unknown_accept`、`FRR_stable`、`miss_drift_all` 与 `drift_acc_all` 之间的权衡。因此，本文将其视为场景调谐参数，并针对不同应用场景继续进行组合搜索。

## 七、当前推荐的参数集

### 平衡型默认参数集
- `gamma_notunk = 1.0`
- `lambda_unkE = 0.045`
- `lambda_stab = 0.02`

### 高安全备选参数集
建议围绕以下区域继续搜索：
- `gamma_notunk = 0.9 ~ 1.0`
- `lambda_unkE = 0.05 ~ 0.055`
- `lambda_stab = 0.015 ~ 0.02`

### 高覆盖探索参数集
建议保留：
- `gamma_notunk = 0.75`
- `lambda_unkE = 0.05`
- `lambda_stab = 0.02`

## 八、下一步实验建议

1. 先固定“默认固化参数”；
2. 以 `gu1__lu0p045__ls0p02` 为新的中心点；
3. 仅对“场景调谐参数”做更系统的组合搜索；
4. 最终输出三类工作点：
   - 平衡型
   - 高安全型
   - 低误拒/业务连续性型

## 九、图像文件为什么可能没看到

根据 summary 中记录的 `run_dir`，图像不是默认保存在 notebook 同目录，而是保存在各自运行目录下：
- v26.2: `../owdc_results/results_wisig_module3_v22_weighted_entry_minimal/run_v26_2__pcA__v22_tuning__manual__20260328_122758`
- v26.3: `../owdc_results/results_wisig_module3_v22_weighted_entry_minimal/run_v26_3__pcA__v22_tuning__manual__20260328_230719`

此外，一部分图是保存在 run 根目录，一部分可能在 split/fold 子目录下。建议直接在对应 `run_dir` 中搜索 `*.png`。
