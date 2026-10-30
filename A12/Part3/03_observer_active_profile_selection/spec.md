# 03 Observer - Active Profile Selection

Source instance: **Active Profile Selection** (`useProfileStore` + its observers, state after CH03).

Subject: a profile store with state `{profile, maturity, pinForm}` (initially no profile, `NONE`, false).
`subscribe(observer)` registers once (set semantics, like zustand's listener Set);
`unsubscribe(observer)` removes it; every `setState` notifies current observers in subscription order.

| Observer | Reaction to a new state | Output |
|---|---|---|
| Hero | re-filters the featured title for the rating | `Hero:<maturity>` |
| ShowsContainer | re-renders rows for the profile | `Rows:<profile>/<maturity>` |
| PinForm | shows the lock screen only when `pinForm` is true | `Pin:<profile>` (nothing otherwise) |

## Input
Commands separated by `;`: `sub <Observer>`, `unsub <Observer>`,
`select <name>:<KIDS|TEEN|ADULT>[:pin]` (sets profile, maturity, pinForm), `signout` (profile `-`, maturity `NONE`, pinForm false).

## Output
All observer outputs joined by `|`, or `-` if there were none. Unknown observer -> `ERROR:unknown observer`.
