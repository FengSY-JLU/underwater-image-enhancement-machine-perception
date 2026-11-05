# Anonymous review artifact

This repository contains a compact, double-anonymous review-stage artifact supporting an underwater image enhancement and machine-perception benchmark. It provides the aggregate numerical tables reported in the accompanying Supplementary Material, the full-precision E4 sign-test/Holm table, and small verification/figure-generation scripts.

## Contents

- `data/`: aggregate E1–E6 tables exported from the accompanying Supplementary Material, plus the full-precision E4 sign-test table.
- `scripts/validate_e4_holm39.py`: independently recomputes the two-sided exact sign tests from positive/negative counts and applies Holm familywise correction across 39 hypotheses.
- `scripts/validate_release_tables.py`: checks aggregate table row counts and basic count identities.
- `scripts/generate_research_question_evolution_figure.py`: source for the conceptual research-question evolution schematic.
- `DATA_PROVENANCE.md`: scope, derivation, and limitations of the shared data.

## Reproduce the E4 statistical check

Python 3.10+ is recommended. Install dependencies and run:

```bash
python -m pip install -r requirements.txt
python scripts/validate_e4_holm39.py
```

The validation script checks all 39 comparisons, verifies that positive, negative, and tied counts sum to 3,370 sources per row, recomputes two-sided exact binomial sign-test p-values after excluding ties, applies Holm correction, and checks the reported 38/39 significance result.

## Scope and limitations

This is a review-stage, aggregate-data artifact. It does **not** contain original benchmark images, annotations, third-party model weights, full source-level per-image records, or the complete inference/training pipeline. It therefore supports inspection of the reported aggregate tables and the E4 statistical correction, but it does not by itself reproduce the underlying image enhancement or perception-model inference. Original datasets and third-party software/weights remain subject to their providers' access and licensing conditions.

No author names, affiliations, personal email addresses, private paths, or non-anonymous title-page files are intentionally included. No open-source reuse license is assigned in this review-stage snapshot; a license can be added to the public post-review release after the authors confirm the intended terms. Please report any apparent anonymization issue through the repository issue tracker without including personal information.
