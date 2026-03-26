# Module3 方法对照表与当前结果解读

这份文档按“技术路线”而不是按代码出现顺序整理。目的是帮助你快速回忆：每个方法到底在改什么、当前结果说明了什么、module2/module3 有没有研究意义。

## 1. 方法对照表（按技术路线）

| 方法 | 样本进入训练的方式 | 监督形式 | unknown 处理 | 稳定化/额外机制 | 一句话定位 |
| --- | --- | --- | --- | --- | --- |
| NoAdapt | 不做 module3 适配 | 无 | 无 | 无 | 所有适配方法的零基线 |
| UngatedAdapt | 所有 target 全进训练 | 硬伪标签 | 无专门 unknown 处理 | 无 | 最朴素自训练，容易把 unknown/错标学进去 |
| GatedAdapt | 先 gate，再训 gated 样本 | 硬伪标签 | 依赖 gate 间接拒识 | 无 | 先筛后学的最早版本 |
| GatedSelfSoft | gate 后训练 | soft pseudo-label | 依赖 gate | 无 | 用 soft 监督减弱错伪标签伤害 |
| GatedProtoAgree | gate + 只收 logit/proto 一致样本 | 硬标签 | 依赖 gate | prototype agreement | 提高 precision，代价是 recall |
| GatedProtoFusionSoft | gate 后训练 | logit+prototype 融合 soft label | 依赖 gate | prototype fusion | 多视角 soft 监督 |
| GatedTriAgree | gate + 三视角一致才收 | 硬标签 | 依赖 gate | logit/proto/kNN agreement | 更保守，precision 更高，recall 更低 |
| GatedTriFusionSoft | gate 后训练 | 三视角融合 soft label | 依赖 gate | 多视角融合 | 从一致性硬门切到融合 soft label |
| ConfThreshSoft | 按置信度阈值选 support | soft pseudo-label | 无专门建模 | tau_conf | 你后来发现 tau_conf 可能贴近 1，导致过硬筛选 |
| AgreementConfSoft | 一致性 + 置信度双筛选 | soft pseudo-label | 无专门建模 | agreement + conf | 比单一阈值更稳，但仍是 hard entry |
| ProtoRefineSoft | 不强依赖复杂 gate，先修伪标签再训 | prototype-refined soft label | 无专门 unknown 候选建模 | prototype refine | coverage 高、易吃到增益，但 purity 和 stable 保真会受影响 |
| ReliableEntropySplit | reliable / unreliable 二分 | reliable 上监督 | unreliable 上高熵/拒识 | entropy regularization | 最早把“不该强学的样本”写进 loss |
| TwoStageUnknown | common vs unknown candidates | common 上监督 | unknown 单独约束 | 两阶段处理 | 把 known/unknown 显式拆开 |
| GCODWFA_Lite | generic split | 软/硬伪标签 | 弱 unknown 约束 | 轻量对齐 | 偏 alignment 驱动 |
| RAINCOAT_Lite | generic split | 伪标签监督 | 有 unknown 分支雏形 | replay/anchor 雏形 | 后续 DG_RAINCOAT 的轻量前身 |
| DG_RAINCOAT_v9-v12 | reliable / ambiguous / unknown | 分桶监督 | unknown 排斥/高熵 | replay + anchor + proto + consistency | DG 三桶框架成形期 |
| DG_RAINCOAT_v13LQ | DG 分桶 | label-quality refined soft label | unknown 分支 | 提升伪标签质量 | 先修 label，再做适配 |
| DG_RAINCOAT_v14Stable | DG 分桶 | soft supervision | unknown 分支 | 更保守的稳定化 | 控制 support 质量差时的过拟合 |
| DG_RAINCOAT_v15QW | DG 分桶 | quality-weighted supervision | unknown 分支 | 质量加权 | 不同 support 不再同权 |
| DG_RAINCOAT_v16QW | DG 分桶 | quality-weighted supervision | unknown 分支 | quality + knownness 决定 align | alignment 也开始挑样本 |
| DG_RAINCOAT_v17LCQ | DG 分桶 | 高质量 support 监督 | unknown 排斥 | local consistency / local density | 你当前很强的 practical baseline 之一 |
| DG_RAINCOAT_v19M2W | 在 v17LCQ 上引入 module2 p_known/p_drift | module2-weighted supervision | module2 扩大 unknown/unrel | module2 guidance + replay | module2 开始真正驱动 module3 |
| DG_RAINCOAT_v19M2W_EnergyU | 同上 | 同上 | unknown 改为 energy-based | energy unknown loss | 当前最强 practical non-oracle 之一 |
| DG_RAINCOAT_v22WeightedEntryMinimal | soft entry：全部 target 进训练但带 sup/stab/unk 权重 | weighted softPL + weighted proto | one-sided unknown energy | residual-norm stable reg | 用于验证“soft entry 能否替代 hard gate”；当前一次实验未真正生效 |
| ThreeBucketV5Soft | reliable / ambiguous / unknown | 分桶监督 | unknown 排斥 | 无 EMA | ThreeBucket 起点 |
| ThreeBucketV5EMA | 同上 | 分桶监督 | unknown 排斥 | teacher EMA | 稳定伪标签 |
| ThreeBucketV5EMAProto | 同上 | 分桶监督 | unknown 排斥 | EMA + 更强 prototype | 抑制 ambiguous 漂移 |
| ThreeBucketV6Curriculum | reliable / ambiguous / weak / unknown | 课程式进入监督 | unknown 排斥 | curriculum | 先不强学 weak 样本 |
| ThreeBucketV7Promotion | 四桶 + promotion | 分阶段提升 weak/ambiguous | unknown 排斥 | sample promotion | 动态提升样本可靠级别 |
| ThreeBucketV8Adaptive_v9-v12 | 成熟 four-bucket | reliable 强、ambiguous/weak 弱监督 | unknown 排斥 | adaptive bucket weighting | ThreeBucket 主体框架定型 |
| ThreeBucketV8Adaptive_v13LQ | V8Adaptive | label-quality refined supervision | unknown 分支 | LQ | 对应 DG 的 LQ 版本 |
| ThreeBucketV8Adaptive_v14Stable | V8Adaptive | soft supervision | unknown 分支 | stable regularization | 对应 DG 的稳定化版本 |
| ThreeBucketV8Adaptive_v15QW | V8Adaptive | quality-weighted supervision | unknown 分支 | QW | 对应 DG 的质量加权版本 |
| ThreeBucketV8Adaptive_v16QW | V8Adaptive | quality-weighted supervision | unknown 分支 | QW + knownness align | 对齐也开始挑样本 |
| ThreeBucketV8Adaptive_v17LCQ | V8Adaptive | 高质量 support 监督 | unknown 排斥 | LCQ | 当前另一条很强的 practical baseline |
| ThreeBucketV8Adaptive_v19M2W | 在 v17LCQ 上接入 module2 | module2-weighted supervision | module2 unknown guidance | module2 guidance | ThreeBucket 和 module2 的结合版 |
| ThreeBucketV8Adaptive_v19M2W_EnergyU | 同上 | 同上 | unknown 改 energy-based | energy unknown loss | ThreeBucket+module2 的较成熟版本 |
| M2V4RouteSplit | module2-v4 直接做主路由：rel/amb/sup/align/unk | generic trainer 上做 supervision | unknown candidate 显式路由 | route-driven generic adaptation | unknown 拒识强，但 stable 误拒也高 |
| M2V4ThreeBucket | module2-v4 主路由 + ThreeBucket 执行 | three-bucket supervision | module2 unknown route | route + bucket | 说明 module2 信息量足够大，但路由可能过硬 |
| OracleGatePseudoAdapt | oracle 路由（已知 target 全纳入） | pseudo label | 无 oracle unknown 问题 | oracle gate | 用来诊断：若 route 完全正确，仅剩 label 误差时会怎样 |
| PredRouteOracleLabelAdapt | predicted route | oracle label | 与当前 route 一致 | oracle label | 用来诊断：route 不变，只把标签改对能提升多少 |
| OracleLabelAdapt | oracle route | oracle label | oracle | oracle upper bound | 适配上界参考，不是可部署方法 |

## 2. 当前实验结果的总体结论

下面这张表使用你当前 `summary_by_protocol.json` 的 4 个 protocol 平均结果，主要看 `drift_acc_all / FRR_stable / FAR_unknown_accept`。

| 方法 | avg drift_acc_all | avg FRR_stable | avg FAR_unknown_accept | 解读 |
| --- | --- | --- | --- | --- |
| NoAdapt | 0.9124 | 0.1757 | 0.0635 | 零基线 |
| ProtoRefineSoft | 0.9277 | 0.2136 | 0.0553 | 高 coverage，但稳定性和 purity 会掉一些 |
| DG_RAINCOAT_v17LCQ | 0.9322 | 0.2037 | 0.0774 | 高 purity、低 recall，偏保守 |
| ThreeBucketV8Adaptive_v17LCQ | 0.9336 | 0.2139 | 0.0758 | 整体均衡，实用性强 |
| M2V4RouteSplit | 0.9222 | 0.3272 | 0.0360 | unknown 拒识很强，但 stable 误拒明显 |
| DG_RAINCOAT_v19M2W_EnergyU | 0.9340 | 0.2324 | 0.0532 | 当前 practical non-oracle 最强之一 |
| ThreeBucketV8Adaptive_v19M2W_EnergyU | 0.9328 | 0.2418 | 0.0504 | 与 DG_v19M2W_EnergyU 接近，略更偏拒识 |
| PredRouteOracleLabelAdapt | 0.9673 | 0.2215 | 0.0518 | 说明 label/entry 仍有较大可挖空间 |
| OracleLabelAdapt | 0.9862 | 0.2168 | 0.0413 | 适配上界 |
| DG_RAINCOAT_v22WeightedEntryMinimal (v22) | 0.8983 | 0.1725 | 0.0704 | 与 NoAdapt 完全一致，本轮不能用于方法优劣判断 |

### 2.1 各条技术路线的表现

- **NoAdapt** 是零基线。后续方法只要高于它，才说明 module3 适配有实际收益。
- **ProtoRefineSoft 路线**：优点是 coverage 高、容易吃到增益；缺点是伪标签 purity 和 stable 保真不一定最好。它适合作为“coverage 派”的代表。
- **DG_RAINCOAT / LCQ 路线**：优点是伪标签很纯、训练更稳；缺点是 support recall 偏低，容易形成“高 precision、低 recall”的硬筛选结构。
- **ThreeBucket 路线**：通常比 DG 稍微放宽一些，整体更均衡；在你现有结果里，它经常与 DG 很接近，属于另一条强 practical baseline。
- **M2V4RouteSplit 路线**：优点是 unknown 拒识很强，FAR_unknown_accept 很低；缺点是 FRR_stable 明显偏高，说明 route 太硬、误伤了 stable。
- **module2 + module3 结合（v19M2W / EnergyU）路线**：这是当前最有价值的 practical 路线之一。它说明 module2 的信息并非没用，但应该以“引导训练入口”的方式介入，而不是直接变成特别硬的路由闸门。
- **Oracle 诊断路线**：不是为了部署，而是为了拆解瓶颈。你现在能清楚看出：`PredRouteOracleLabelAdapt` 远强于 `OracleGatePseudoAdapt`，说明主瓶颈在 label/entry，而不是 adapter 完全不会学。
- **v22 WeightedEntry-Minimal**：这条路线的研究命题是对的，但当前一次实验没有真正形成有效检验，因为结果与 NoAdapt 完全一致，更像实现链路未生效，而不是方法被否证。

### 2.2 从 selection 统计看，真正的瓶颈是什么

| 方法 | avg sel_precision | avg sel_recall | avg pseudo_acc_selected | 解读 |
| --- | --- | --- | --- | --- |
| ProtoRefineSoft | 0.7006 | 0.4811 | 0.9333 | coverage 高 |
| DG_RAINCOAT_v17LCQ | 0.7574 | 0.2882 | 0.9769 | purity 高，但 recall 低 |
| ThreeBucketV8Adaptive_v17LCQ | 0.7456 | 0.3381 | 0.9723 | 比 DG 略放宽，较均衡 |
| M2V4RouteSplit | 0.6948 | 0.4606 | 0.9374 | coverage 高，unknown_cand_precision≈0.8725 |
| OracleGatePseudoAdapt | 1.0000 | 1.0000 | 0.9117 | route 完美但 label 仍有误差 |
| PredRouteOracleLabelAdapt | 1.0000 | 0.4606 | 1.0000 | label 完美但 route 仍限制 coverage |

从这张表可以看出：
- 你当前最强的 practical 方法并不是 purity 不够，而是 **coverage 不足**。
- `DG_RAINCOAT_v17LCQ / v19M2W_EnergyU` 这类方法的 `pseudo_acc_selected` 已经很高，但 `sel_recall` 只有 0.29 左右，说明进训练的 target 可适配样本太少。
- `M2V4RouteSplit` 能把 `sel_recall` 拉到 0.46 左右，同时 `unknown_cand_precision` 很高，但代价是 stable 被误伤太多。
- `PredRouteOracleLabelAdapt` 和 `OracleGatePseudoAdapt` 的对照说明：当前最大 gap 不在“route 完不完美”，而在“进入训练的样本一旦选中，标签是否足够可靠”。

## 3. module2 和 module3 到底有没有意义？

### 3.1 module2 有意义，而且非常有意义

有三点证据：
1. `M2V4RouteSplit` 的 `FAR_unknown_accept` 很低，说明 module2 里 stable/unknown/drift 的路由信息不是噪声，而是真能提高 unknown 拒识。
2. `DG_RAINCOAT_v19M2W_EnergyU` 比 `NoAdapt` 平均 `drift_acc_all` 高约 2.16 个点（0.9340 vs 0.9124），说明 module2 的输出进入 module3 之后，能转化为实际适配收益。
3. 但 `M2V4RouteSplit` 的 `FRR_stable` 很高，说明 module2 **不能直接当硬裁决器**。它更适合作为连续引导信息，而不是单独决定“谁能进训练”。

### 3.2 module3 也有意义，但你当前最强价值在“诊断与接口设计”，不只是再堆 loss

module3 的意义不只是把 accuracy 拉高，而是把问题拆开。当前结果至少说明：
1. **适配本身是有用的**。多个 non-oracle 方法都明显优于 NoAdapt。
2. **adapter 容量不是主瓶颈**。Oracle 结果离当前最强 non-oracle 还有明显 gap，说明不是“学不动”，而是“训练入口和标签质量还没打通”。
3. **module3 目前最值得做的不是继续堆复杂 loss，而是把 module2 到 module3 的接口从 hard gate 改成 soft entry / continuous weighting。**

## 4. 你现在这条研究路线值不值得继续？

值得，而且方向没有跑偏。

更准确地说，你现在做的已经不是普通闭集 UDA，而是在做：
- 开集 / 通用域适应
- 带 unknown 的测试时自适应
- module2 负责结构化路由，module3 负责条件式适配

这条路线的研究意义在于：
1. 你已经证明了 **route 信息有用**；
2. 你也证明了 **直接 hard route 不够好**；
3. 你进一步通过 oracle 拆解证明了 **主瓶颈在 training entry / label side**；
4. 因此后续工作完全可以围绕“从离散路由走向连续加权适配”展开。

## 5. 我对当前阶段的判断

### 5.1 你做的 module2 有研究意义吗？
有，而且它已经证明了“分 stable / drift / unknown”不是伪命题。只是当前还不能把它当最终裁决器，只能把它当 **高信息量先验**。

### 5.2 你做的 module3 有研究意义吗？
有，而且它最大的意义在于提供了一个可检验平台：你已经能清楚地区分“selection 问题、label 问题、适配问题、unknown 问题”。这对博士课题是非常重要的。

### 5.3 接下来最值得做什么？
不是再扩方法树，而是把 `v22 = WeightedEntry-Minimal` 真正跑通，并监控 `effective_coverage / sum_w_sup / soft_pseudo_acc`。只有当这条线真正生效后，第二阶段再谈 teacher、EMA prototype、known-side energy 才有意义。

## 6. 一句话结论

你的 **module2 有意义，module3 也有意义**。当前结果并不是“路线不对”，而是已经很明确地把博士工作的主问题定位出来了：**如何让 module2 给出的 stable/drift/unknown 信息，以连续、可学习的方式进入 module3，而不是作为过硬的闸门。**