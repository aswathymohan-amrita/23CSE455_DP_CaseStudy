# CH01 - Explicit class review state

Existing features: CommandCreateClass already supports stereotypes, $tags, colors,
URLs, generics and inheritance. The extension is a constrained model property,
not a replacement for those annotations.

Syntax: `class Order [review=pending]`. Values: pending, approved, rejected
(case-insensitive). The suffix comes last, after an optional empty `{}` body.
Use a single-line declaration, followed by separate member lines if needed.
Multiline declaration syntax is not extended. Omission on redeclaration preserves
the previous status; a later explicit status overwrites it.

Acceptance: valid status stored on Entity and visible in the class header; unknown
value is rejected; class/link counts stay unchanged; existing syntax, stereotype
and explicit color still work; PNG and SVG render. Review annotation applies to
class-like types handled by CommandCreateClass. The sample and acceptance suite
exercise class nodes. Text/XMI/other serializers are not extended.

Implementation: parser regex and executeArg, Entity accessors, and header Display.
No new command class is needed. Command is modified; Factory Method, layout
Strategy, text-block Composite and VizJs Adapter are preserved.
