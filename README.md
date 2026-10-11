# 23CSE455 — Design Patterns Case Study


This repository contains information about case study, **Design Pattern Identification and Evolution in a Laravel-Based Healthcare Management Application**. It documents a source-based architectural review, three hypothetical integration changes, eight proposed design-pattern collaborations, cross-language demonstrations, reproducible tests, and a compiled academic report.

## Submission

| Resource | Location |
| --- | --- |
| Team A5 overview, setup and evidence | [A5/README.md](A5/README.md) |
| Final compiled report (PDF) | [A5/A5_Report.pdf](A5/A5_Report.pdf) |
| Editable report source (LaTeX) | [A5/A5_Report.tex](A5/A5_Report.tex) |
| Baseline pattern identification | [A5/Part1/](A5/Part1/) |
| Evolution scenarios and PHP prototypes | [A5/Part2/](A5/Part2/) |
| Cross-language source and measurements | [A5/Part3/](A5/Part3/) |
| Installable Laravel 12 integration overlay | [A5/laravel_integration/](A5/laravel_integration/) |
| Automated validation workflow | [.github/workflows/a5-validate.yml](.github/workflows/a5-validate.yml) |

## Scope and evidence

The inspected application is [esteham/hospital-management](https://github.com/esteham/hospital-management), fixed at commit `1e7420e431771e3f5eec470d8a005e8255fa5fe8`. **Existing patterns and newly proposed patterns are deliberately distinguished.** The original source excerpts are in `A5/data/code/`; the proposed implementations are case-study extensions, not claims about patterns already present in the baseline.

The extension demonstrates **eight patterns**, with a proposed two-pattern allocation for each of four members. All eight also have standalone Java, Python, JavaScript and C++ examples (32 programs). An additional Laravel overlay integrates three protected HTTP endpoints and is tested against a clean upstream checkout using simulated provider responses. It does **not** replace the upstream application's existing booking workflows or connect to real payment, laboratory or EHR providers.

## Validation

[GitHub Actions](.github/workflows/a5-validate.yml) checks the PHP contracts, 32 language programs, reproducible process timings, Laravel overlay tests, and LaTeX compilation. A successful workflow run provides evidence of those checks, not proof of live third-party integration.

For exact commands, dataset locations, limitations and attribution, read [the full Team A5 README](A5/README.md). The academic report is the primary narrative deliverable.


## Team

- Nemali Ashrith Reddy — AM.AL.U4AID23014
- Akshay Reddy Velugati — AM.AL.U4AID23062
- B. Pravallika — AM.SC.U4CSE23212
- Daripineni Manogna — AM.SC.U4CSE23022
