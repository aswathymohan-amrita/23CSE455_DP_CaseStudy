# 04 Decorator - Persisted Profile Store

Source instance: **Persisted Profile Store** (`data/code/src/stores/profile.ts:12-27`: `devtools(persist(creator))`).

Component `ProfileStore`: `set(field, value)`, `state()`, `clearStorage()`.
- `BasicStore` (ConcreteComponent): fields `profile` (initially `null`) and `pinForm` (initially `false`);
  any other field -> error `unknown field <f>`; `clearStorage()` -> error `clearStorage not available`.
- `PersistDecorator`: after each successful `set`, writes `state()` to storage key `test-store`;
  `clearStorage()` removes the key.
- `DevtoolsDecorator`: after each successful `set`, appends `set <field>=<value>` to the devtools log;
  forwards `clearStorage()`.

## Input
`decorators;ops`. `decorators` = `none` or names joined by `+`, **innermost first**
(`persist+devtools` = `devtools(persist(base))`, as in the source). `ops` = comma list of
`<field>=<value>`, `clear`, or `-`.

## Output
`state=<profile=..&pinForm=..>;storage=<value of test-store or ->;log=<entries joined by , or ->`
Errors: `ERROR:<message>`; unknown decorator -> `ERROR:unknown decorator <name>`.
