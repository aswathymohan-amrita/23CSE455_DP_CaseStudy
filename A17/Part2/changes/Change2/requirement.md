# CH02 - Review-state fill policy

Existing style rules already resolve stereotypes and explicit colors. Add
`!pragma classReviewPalette default|pastel|mono` as a review-aware fill policy.
The default delegates to existing style behavior. Pastel: pending #FFF3CD,
approved #D4EDDA, rejected #F8D7DA. Mono: all reviewed classes #EEEEEE.
Explicit class fill overrides the policy; unreviewed classes keep existing styles.
The policy intentionally leaves typography, borders and explicit header styling
to existing rules. Put the pragma before declarations for clear input intent.

Acceptance: both palettes render, explicit fill wins, invalid or missing values
are rejected, default output is unchanged. ReviewPalette.Pastel and .Mono
implement a new Strategy collaboration. CommandPragma is modified; the original
layout Strategy instance is not renamed or counted twice.
