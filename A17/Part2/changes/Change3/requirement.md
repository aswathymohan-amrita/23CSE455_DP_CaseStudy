# CH03 - Opt-in SVG review metadata and local style refactoring

Existing SVG contains entity IDs, qualified names and source locations. Add
`!pragma svgReviewMetadata true|false` for machine-readable review information.
Default: off. Enabled: reviewed entity groups carry data-review-status. Unreviewed
entities omit it. Invalid or missing values are rejected. PNG keeps the visible
diagram and receives no new SVG attribute. No new output format is claimed.

Trace: CommandPragma -> Pragma -> EntityImageClass -> UGroupType ->
PortableSvgDocument.setAttribute. The serializer allow-list must be extended:
adding only the enum and group data silently loses the new attribute.

Refactoring: drawInternal used repeated getStyle() lookups. Introduce local
resolvedStyle and reuse the stable result for shadow, border, fill and stroke.
This removes repeated merge requests without changing rendering decisions.
Byte-identical CH02/CH03 review.svg (metadata off) verifies the recorded example.
No new Factory, Composite or Adapter collaboration is introduced by this option.
