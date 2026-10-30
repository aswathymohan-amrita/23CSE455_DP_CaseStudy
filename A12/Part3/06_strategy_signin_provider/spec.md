# 06 Strategy - Sign-in Provider Strategy

Source instance: **Sign-in Provider Strategy** (`authOptions.providers` in `data/code/src/server/auth.ts:38-64`; NextAuth
selects the provider by id at sign-in). The source configures only Google; the commented block
documents adding more, which this problem exercises.

Strategy `Provider { id; authorize(credential) -> profile id or failure }`:
| id | accepts | profile id |
|---|---|---|
| `google` | credential starting `g-` | `google:<rest>` |
| `github` | credential starting `gh-` | `github:<rest>` |
| `email` | `local@domain` with a `.` in the domain | `email:<lower-cased address>` |

Context `NextAuth(providers)`: `signIn(providerId, credential)`.

## Input
`providers;providerId;credential`, `providers` = comma list configured in this order.

## Output
`OK:<profile id>`, `ERR:unknown provider` (id not configured), `ERR:invalid credentials`,
or `ERROR:unsupported provider <id>` when the configuration names a provider that does not exist.
