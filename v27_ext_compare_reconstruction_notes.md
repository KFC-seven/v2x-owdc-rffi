# External comparison reconstruction notes

This package uses `wisig_module3_adaptation_suite_v25.ipynb` as the base and reconstructs a compact external-comparison suite.

## Internal representative methods
- `NoAdapt`
- `ProtoRefineSoft`
- `M2V4RouteSplit`
- `DG_RAINCOAT_v19M2W_EnergyU`
- `DG_RAINCOAT_v22WeightedEntryMinimal` (balanced default work point)

## External baselines (paper/repo-guided reconstructions under unified WiSig backbone + Module2 evaluation)
- `PCPD_recon`
- `OVANet_recon`
- `COMET_recon`
- `JRFFP_SC_recon`

## Important note
These external baselines are **not claimed to be byte-for-byte reproductions** of the official repositories/papers.
They are **embedding-space reconstructions** integrated into the same WiSig backbone / split / evaluation pipeline so that:
1. data reuse is consistent,
2. protocol splits are identical,
3. open-set metrics are directly comparable.

## Default balanced parameter set
The v22 baseline is initialized at:
- `gamma_notunk = 1.0`
- `lambda_unkE = 0.045`
- `lambda_stab = 0.02`

This is used as the current balanced reference work point for external comparison.
