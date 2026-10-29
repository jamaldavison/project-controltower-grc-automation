# Project ControlTower — Enterprise IT Controls & Continuous Compliance Automation

**Jamal Davison | Cybersecurity / GRC engineering portfolio**

> **Independent educational simulation.** All systems, evidence references, owners, and review outcomes are fictional. No employer data was accessed. Metadata quality checks do **not** establish that controls operate effectively or satisfy PCI DSS or SOC 2.

## Business problem

Audit preparation often requires manual reconciliation of access reviews, changes, vulnerability work, backup tests and incident records. ControlTower demonstrates an offline Python pipeline that flags incomplete or late *evidence metadata* and produces repeatable reports for human inspection.

## Project architecture

Synthetic CSV → schema validation → rule-based exception checks → CSV results + JSON summary + Markdown dashboard → human review (not automated).

[Architecture diagram](docs/ARCHITECTURE.md)

## Results from 12 synthetic records (2026-10-29)

| Metric | Fictional sample |
|---|---:|
| Records evaluated | 12 |
| Flagged for review | 6 |
| Ready for manual sample review | 6 |
| Overdue and unapproved | 5 |
| Unit tests passed | 2 of 2 |

These are checks on **invented examples**, not actual control tests or verified audit evidence.

## Explore the project

| Artifact | Link |
|---|---|
| Python validation engine | [src/controltower.py](src/controltower.py) |
| Fictional evidence dataset | [data/sample_evidence.csv](data/sample_evidence.csv) |
| Automated unit tests | [tests/test_controltower.py](tests/test_controltower.py) |
| Control catalog | [docs/CONTROL_CATALOG.md](docs/CONTROL_CATALOG.md) |
| Data dictionary | [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) |
| Assessment test plan | [docs/TEST_PLAN.md](docs/TEST_PLAN.md) |
| Security & limitations | [docs/SECURITY_AND_LIMITATIONS.md](docs/SECURITY_AND_LIMITATIONS.md) |
| Generated summary | [outputs/summary.json](outputs/summary.json) |
| Sample dashboard | [outputs/dashboard.md](outputs/dashboard.md) |
| Lovable integration notes | [website/LOVABLE_INTEGRATION_PROMPT.md](website/LOVABLE_INTEGRATION_PROMPT.md) |

The Excel dashboard is available in the downloadable portfolio package; upload of that binary file to this repository is pending.

## Try it locally

Requires Python 3.10+; **no third-party dependencies**.

```bash
python src/controltower.py --input data/sample_evidence.csv --out outputs --as-of 2026-10-29
python -m unittest discover -s tests -v
```

## Scope of implementation

**Implemented and locally tested:** CSV parsing, basic schema/record checking, deterministic evidence-metadata flagging, CSV/JSON/Markdown generation, two automated unit tests.

**Not implemented:** actual data integrations, authentication, evidence collection, verified control testing, live remediation, risk scoring or compliance determination.

## Professional relevance

This project demonstrates reproducible security-governance automation concepts in five domains: access governance, change control, vulnerability management, backup and restore, and incident management.

[Visit my living résumé](https://jamal-davison-live-resume.lovable.app/).
