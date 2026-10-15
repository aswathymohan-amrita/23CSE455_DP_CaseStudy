# Candidate decisions

Observation scope: five requested GoF pattern types in the class declaration,
relationship, class-header and layout/export path. This is not a repository census.

Confirmed: Command dispatch, Factory Method product creation, Strategy backend
selection, Composite text-block composition and Adapter VizJs output conversion.

Rejected (2 observations):
1. Treating Entity/Link membership alone as Composite. A graph of model objects is
   insufficient proof of a shared recursive component operation. The rendering
   text-block tree supplies that evidence instead.
2. Calling UGraphicDelegator an Adapter merely because it forwards calls. It wraps
   the same UGraphic contract; the inspected delegation does not establish an
   incompatible-interface conversion. Decorator is a plausible separate analysis,
   outside the five-type candidate scope.

Uncertain (1 observation): the older draft's PlacementStrategy collaboration was
not fully mapped to a client on the selected input path. It is not counted as a
confirmed additional Strategy instance. The backend-selection instance has a
concrete context and selection site, and is used in the final inventory.

Template Method in the parsing skeleton and graphics decorators are supporting
idioms, not an exhaustive second inventory. The five-type scope follows the
case-study brief; no faculty approval of this narrower scope is asserted.
