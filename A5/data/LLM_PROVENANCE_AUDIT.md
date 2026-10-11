# LLM evidence provenance and verification audit

The faculty instructions require an **exact prompt, the exact input, a raw model response and human source/test verification** for each recorded LLM analysis. The existing `Part1/llm.csv`, `Part2/llm.csv`, `Part3/*/llm/llm.csv` and `data/llm.csv` are retained as historical records; this audit does **not** invent prompts or model responses.

| Part | Present | Limitation |
| --- | --- | --- |
| Part 1 discovery | Pattern CSV, source excerpts, `Part1/llm/verification.md` and Gemini thread identifier | `Part1/llm.csv` links to a verification note as a prompt and to a report section as model output. Neither establishes a complete verbatim raw exchange. |
| Part 2 evolution | Source-change records, code, diagrams and `Part2/llm.csv` | The exact original prompt and raw response are not independently archived as distinct files. |
| Part 3 cross-language | Adapter and Strategy prompt files, runnable source and captured output in `data/test_result/` | Source-code directories and program stdout are not necessarily the raw LLM response; do not treat them as equivalent. |
| Eight-pattern extension | New source, test suite and CI results | Do not retroactively label generated examples as a specific recorded LLM interaction without a real transcript. |

**Human verification:** inspect the baseline controller/model excerpts at the pinned commit; run PHP contracts; run the cross-language suite; install and test the overlay using HTTP fakes. These checks validate code behavior but **cannot reconstruct a missing raw LLM transcript**.

**To close the remaining evidence gap:** team members must export their actual historical Gemini/ChatGPT conversations, preserving the real date, displayed model, exact prompt, exact supplied code and exact raw response. Put those text files under `Part1/llm/`, `Part2/llm/` and `Part3/llm/`, then update `data/llm.csv` to reference the files. If the original transcripts are unavailable, mark those interactions `cannot_confirm`; do not fabricate them.

The Gemini thread identifier in the original records is not itself a locally archived raw model response. This is a **documented evidence limitation**, not a test failure.
