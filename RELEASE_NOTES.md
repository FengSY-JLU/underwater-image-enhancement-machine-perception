# Review-stage artifact notes

## Baseline: 2026-11-05

The initial public review artifact comprised 11 derived aggregate CSV tables, three small verification/figure-generation scripts, the README, provenance note, requirements and checksum list. The submitted manuscript's experimental statements and statistical outputs are frozen in that baseline.

## Documentation and aggregate-validation update: 2026-11-07

The patch adds a reviewer-oriented protocol map and data dictionary, together with a standard-library script checking high-level numerical statements directly from the **existing** aggregate CSV tables. It also improves the README's limitations and validation instructions. This update is not a rerun or revision of the underlying experiment.

The patch must **not** change any of the 11 baseline `data/*.csv` files, `scripts/validate_e4_holm39.py`, `scripts/validate_release_tables.py`, `scripts/generate_research_question_evolution_figure.py` or `requirements.txt`.

Future additions such as source-level derived records, inference pipelines, environmental manifests or output figures should be audited for provenance, third-party rights, anonymization, geometry and checkpoint identity before being described as available. New or changed experimental results should be versioned explicitly rather than silently overwritten.
