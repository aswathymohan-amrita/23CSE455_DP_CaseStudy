# Verification record

Automated reviewer: scripts and source checks performed during this assistant run.
Human reviewer: not yet recorded. Neither named student is claimed to have
personally reviewed code or performed tests that the assistant actually ran.

Discovery: partial initial output. The annotated tag-object hash was initially
described as a commit, then corrected using the cloned repository. Final baseline
commit is 149874a1bb2b64c42889d7178cb89f6647ac14bc. The older placement inventory
lacked a mapped context; it was excluded and recorded as uncertain.

Evolution: partial initial implementation. The first metadata attempt omitted
PortableSvgDocument's allow-list. The integration test failed; the serializer was
fixed. A mono-palette assertion also assumed six-digit SVG colors; it was corrected
after inspecting the valid #EEE output. Final results: baseline 3/3, CH01 11/11,
CH02 15/15, CH03 20/20; full built JAR 20/20. Upstream baseline/final failures match.

Cross-language: all 16 shared cases passed for each language. Source code is
AI-generated in this interaction; tests are separate. Timing follows one warm-up
and five measured processes and is dominated by startup for these tiny inputs.

Human verification tasks: read each participant mapping against source; run both
test scripts; inspect all three example diagrams; explain the serializer fix;
check team contributions, faculty approval, model/tier requirement and upload.
Record actual reviewer/date/claim/correction in human_verification.csv.
