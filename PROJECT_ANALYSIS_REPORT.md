# Project Analysis Report

## Scope

This report is based on a full inventory of the current workspace:

- 80 notebooks
- 1 Python script
- 5 Markdown notes
- 0 test files discovered
- 0 dependency manifests discovered (`requirements.txt`, `pyproject.toml`, `environment.yml`, etc.)

The evaluation standard here is "research-code quality", not production software quality. So a `LOW` score does not mean "bad research"; it usually means "hard to reuse, reproduce, or maintain".

## Executive Summary

Your project is a strong and coherent RF fingerprinting research line around:

- open-world / domain-continual RF fingerprinting
- module2 for structured diagnosis / routing
- module3 for selective adaptation under unknown-vs-drift uncertainty
- cross-domain validation on WiFi / WiSig / LTE-V

From the notes and the notebook evolution, the scientific story is already clear:

- `module2` is meaningful, but it works best as a soft prior rather than a hard gate.
- `module3` is meaningful, but the main bottleneck is not adapter capacity.
- The current real bottleneck is training entry quality and pseudo-label reliability/coverage.
- The most valuable next step is not "adding more losses", but turning routing signals into continuous weighting.

In short: the research direction is good, the decomposition is meaningful, and the scientific diagnosis is already deeper than a typical "just stack another method" project.

## Scientific Assessment

### What is already strong

- The project is not a random collection of notebooks. It has a visible method evolution path.
- The problem decomposition is strong: stable / drift / unknown are treated as structurally different cases.
- The project has both internal method ablations and external comparison notes.
- The notes in `module3_methods_comparison_and_assessment.md`, `v26_parameter_analysis_and_fixed_vs_scenario_params.md`, and `v30_module3_results_tables.md` show mature reflection, not just raw experimentation.

### What the current evidence says

- The route information learned in `module2` has value.
- Direct hard routing is too aggressive and hurts stable samples.
- The strongest practical gains come when `module2` informs `module3`, not when it fully decides entry.
- Oracle comparisons suggest the biggest gap is on entry / label quality, not model capacity.
- The `v22 WeightedEntry-Minimal` direction is scientifically well-motivated and worth continuing.

### My judgment on the research value

- The project has clear dissertation-level value.
- The most original part is not a single loss term. It is the interface design between diagnosis and adaptation.
- Your work is already beyond a standard closed-set UDA story. It is closer to open-world, unknown-aware, deployment-oriented adaptation.

## Engineering Assessment

### Global strengths

- The project has unusually rich experimental logging and version traceability.
- Many notebooks are heavily functionized instead of being pure one-off cells.
- The WiFi `module2` line is relatively readable and close to "reproducible research notebook" quality.
- The early WiSig `module3` notebooks are compact enough to serve as conceptual baselines.

### Global weaknesses

- The repo is a research workbench, not a packaged experiment framework.
- The `README.md` is too short to support a new reader.
- There is no environment specification, no dependency lock file, and no test suite.
- Hardcoded paths are common.
- A large part of the codebase lives inside giant notebooks.
- The `wisig_module3_adaptation_suite` family contains 44 versions, which makes maintenance difficult.
- Some final notebooks were saved with partial execution state, which is risky for reproducibility.

### Bottom-line engineering verdict

- Research strength: `HIGH`
- Reproducibility as a fresh checkout: `LOW`
- Maintainability for the original author: `MID`
- Maintainability for a collaborator/new student: `LOW`

## Best Entry Points

If a new collaborator had to understand the project quickly, I would recommend starting from:

1. `module3_methods_comparison_and_assessment.md`
2. `wifi_module2_streamlined_joint_router.ipynb`
3. `wisig_module3_v2_conf_gated.ipynb`
4. `wisig_module3_pseudo_suite_fixed_v2.ipynb`
5. `wisig_module3_adaptation_suite_v36.3.ipynb`
6. `ltev_module3_adaptation_suite_v2.1.ipynb`

That order moves from concept -> compact implementation -> mature large-scale adaptation suite.

## Biggest Risks

- The most important scientific logic is spread across versioned notebooks instead of extracted modules.
- Final-stage WiSig and LTE-V notebooks are closer to embedded experiment platforms than reusable scripts.
- Path coupling to `../ManySig.pkl`, `../owdc_results/...`, `E:/rf_datasets_IQ_raw`, and related directories will block outside reuse.
- Without a unified runner/config layer, it is too easy to mis-run a historical notebook with stale assumptions.

## Most Important Refactoring Opportunities

1. Extract shared loaders, metrics, router logic, and adaptation loops into a small `src/` package.
2. Replace hardcoded paths with a single config object or YAML/JSON profile.
3. Keep only a few canonical notebooks per track, and archive the rest as history.
4. Add one reproducibility document: dataset layout, required files, and the exact "run this first" notebooks.
5. Add lightweight smoke tests for loaders, metrics, and routing/adaptation primitives.

## Score Legend

`R` = robustness, `U` = usability.

Issue codes:

- `PATH`: many hardcoded paths or path-coupled assumptions
- `BIG`: large notebook/script with broad responsibility
- `HUGE`: giant notebook, closer to a platform than a single experiment
- `FAMILY`: one member of a very large copy-evolve notebook family
- `PARTEXEC`: saved with partial execution state
- `NOMD`: no Markdown guidance
- `LOWDOC`: documentation exists but is too thin

Strength codes:

- `FUNC`: logic is functionized rather than purely inline
- `DOC`: good experiment notes / markdown structure
- `REPRO`: relatively suitable as a reproducible research notebook
- `LOWPATH`: relatively low path coupling
- `SMALL`: small standalone tool

## Documentation Assessment

- `README.md`: scientifically correct but too short; weak onboarding value.
- `module3_methods_comparison_and_assessment.md`: excellent method map.
- `v26_parameter_analysis_and_fixed_vs_scenario_params.md`: strong paper-writing support note.
- `v27_ext_compare_reconstruction_notes.md`: concise but useful framing note.
- `v30_module3_results_tables.md`: strong result-summary artifact.

## Per-File Assessment

| File | R | U | Issues | Strengths |
| --- | --- | --- | --- | --- |
| `detect_dmrs_domain.py` | MID(3) | MID(3) | PATH | FUNC,SMALL |
| `LTE-V_eq.ipynb` | LOW(2) | LOW(1) | NOMD,PATH | - |
| `lte_class_domain_score.ipynb` | LOW(2) | LOW(1) | NOMD,PATH | - |
| `ltev_module3_adaptation_suite_v1.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE | FUNC,DOC |
| `ltev_module3_adaptation_suite_v2.1.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE | FUNC,DOC |
| `ltev_module3_adaptation_suite_v2.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE | FUNC,DOC |
| `wifi_class_domain_score.ipynb` | MID(3) | LOW(1) | NOMD | - |
| `wifi_class_domain_score_brainstorm_scores.ipynb` | LOW(2) | MID(3) | PATH | REPRO |
| `wifi_class_domain_score_dom_variants_txrandom.ipynb` | MID(3) | LOW(2) | LOWDOC | - |
| `wifi_class_domain_score_perRxDay.ipynb` | MID(3) | LOW(1) | NOMD | - |
| `wifi_class_domain_score_perRxDay_stratified.ipynb` | HIGH(4) | LOW(1) | NOMD | LOWPATH |
| `wifi_module2_final_gate.ipynb` | MID(3) | HIGH(4) | - | REPRO |
| `wifi_module2_final_gate_sidscan.ipynb` | MID(3) | HIGH(4) | - | REPRO |
| `wifi_module2_final_gate_v2_dualthreshold.ipynb` | LOW(2) | MID(3) | PATH | REPRO |
| `wifi_module2_final_streamlined.ipynb` | MID(3) | HIGH(4) | - | REPRO |
| `wifi_module2_final_streamlined_protocol_sweep_errstats.ipynb` | MID(3) | HIGH(5) | - | DOC,REPRO |
| `wifi_module2_sr1_support_region_diagnosis.ipynb` | HIGH(4) | HIGH(5) | - | DOC,LOWPATH,REPRO |
| `wifi_module2_sr1_support_region_diagnosis_errstats.ipynb` | HIGH(4) | HIGH(5) | - | DOC,LOWPATH,REPRO |
| `wifi_module2_streamlined_joint_router.ipynb` | HIGH(4) | HIGH(5) | - | FUNC,DOC,REPRO |
| `wifi_module2_v1.ipynb` | MID(3) | HIGH(4) | FAMILY | DOC,REPRO |
| `wifi_module2_v2.ipynb` | MID(3) | MID(3) | FAMILY | REPRO |
| `wifi_module2_v3.ipynb` | HIGH(4) | HIGH(4) | FAMILY | DOC,LOWPATH,REPRO |
| `wifi_module2_v4.ipynb` | HIGH(4) | HIGH(4) | FAMILY | DOC,LOWPATH,REPRO |
| `wifi_module2_v5.ipynb` | HIGH(4) | LOW(2) | FAMILY | FUNC |
| `wifi_module2_v6.ipynb` | MID(3) | MID(3) | PATH,FAMILY | FUNC,DOC,REPRO |
| `wifi_module2_v7.1.ipynb` | MID(3) | LOW(1) | LOWDOC,PATH,FAMILY | FUNC |
| `wifi_module2_v7.ipynb` | MID(3) | LOW(1) | LOWDOC,PATH,FAMILY | FUNC |
| `wifi_module2_v8.ipynb` | MID(3) | LOW(1) | LOWDOC,PATH,FAMILY | FUNC |
| `wisig_module3_adaptation_suite_v10.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v11.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v12.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v13.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v14.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v15.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v16.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v17.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v18.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v19.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v20.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v21.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v22.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v23.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v24.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v25.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v26.1.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v26.2.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v26.3.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v27.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v28.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v29.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v3.ipynb` | HIGH(4) | MID(3) | FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v30.1.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v30.2.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v30.3.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v30.4.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v30.5.ipynb` | LOW(1) | LOW(1) | LOWDOC,PATH,BIG,HUGE,FAMILY | FUNC |
| `wisig_module3_adaptation_suite_v30.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v31.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v32.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v33.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v34.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v35.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v36.1.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v36.2.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,PARTEXEC,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v36.3.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,PARTEXEC,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v36.ipynb` | LOW(1) | LOW(1) | PATH,BIG,HUGE,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v4.ipynb` | HIGH(4) | MID(3) | FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v5.ipynb` | MID(3) | LOW(2) | PATH,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v6.ipynb` | MID(3) | LOW(2) | PATH,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v7.ipynb` | MID(3) | LOW(2) | PATH,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v8.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_adaptation_suite_v9.ipynb` | LOW(2) | LOW(1) | PATH,BIG,FAMILY | FUNC,DOC |
| `wisig_module3_gated_adaptation_complete.ipynb` | MID(3) | HIGH(4) | - | REPRO |
| `wisig_module3_gated_adaptation_topq.ipynb` | MID(3) | HIGH(5) | - | DOC,REPRO |
| `wisig_module3_pseudo_suite.ipynb` | HIGH(4) | HIGH(5) | - | FUNC,DOC,REPRO |
| `wisig_module3_pseudo_suite_fixed.ipynb` | HIGH(4) | HIGH(5) | - | FUNC,DOC,REPRO |
| `wisig_module3_pseudo_suite_fixed_v2.ipynb` | HIGH(4) | HIGH(5) | - | FUNC,DOC,REPRO |
| `wisig_module3_sr1_anchored_local_stats.ipynb` | LOW(2) | LOW(2) | PATH,BIG | FUNC,DOC |
| `wisig_module3_v22_debug.ipynb` | LOW(2) | LOW(2) | PATH,BIG | FUNC,DOC |
| `wisig_module3_v2_conf_gated.ipynb` | HIGH(4) | HIGH(5) | - | FUNC,DOC,REPRO |
| `wisig_module3_v2_false_drift_sweep.ipynb` | HIGH(4) | HIGH(5) | - | FUNC,DOC,REPRO |

## File-Level Commentary

### Strongest code artifacts

- `wifi_module2_streamlined_joint_router.ipynb`
- `wifi_module2_sr1_support_region_diagnosis.ipynb`
- `wifi_module2_sr1_support_region_diagnosis_errstats.ipynb`
- `wisig_module3_v2_conf_gated.ipynb`
- `wisig_module3_v2_false_drift_sweep.ipynb`
- `wisig_module3_pseudo_suite_fixed_v2.ipynb`

These are the files I would trust most for onboarding another researcher.

### Weakest engineering artifacts

- `wisig_module3_adaptation_suite_v23.ipynb` through `wisig_module3_adaptation_suite_v36.3.ipynb`
- `ltev_module3_adaptation_suite_v1.ipynb`
- `ltev_module3_adaptation_suite_v2.ipynb`
- `ltev_module3_adaptation_suite_v2.1.ipynb`

These are scientifically rich, but engineering-heavy and hard to reuse because of size, path coupling, and version sprawl.

### Special note on `detect_dmrs_domain.py`

This is the only conventional script in the repo. It is actually a good seed for cleaner tooling:

- functions are clearly separated
- CLI exists
- logic is understandable

But it still needs:

- path configuration instead of a built-in default absolute path
- stronger input validation around MAT structure assumptions
- unit tests for heuristic thresholds

## Final Conclusion

This repository already contains a valuable research program.

What is missing is not scientific direction. What is missing is a thin engineering shell around the scientific core:

- one canonical data config
- one canonical runner per track
- one extracted shared module layer
- one short reproducibility guide

If you invest in those four things, the project will become much easier to defend, share, and publish from.
