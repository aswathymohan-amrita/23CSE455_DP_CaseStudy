# 05 Adapter - NextAuth Prisma Persistence Adapter

Source instance: **NextAuth Prisma Persistence Adapter** (`PrismaAdapter(prisma)` in `data/code/src/server/auth.ts:48`,
`@next-auth/prisma-adapter` `dist/index.js:206-264`).

- **Target** `AuthAdapter` (what the auth library calls): `createUser(email, name) -> User`,
  `getUserByEmail(email) -> User | none`, `linkAccount(userId, provider) -> Account`.
- **Adaptee** `OrmClient` (Prisma-like, different shape): `user.create(data)`, `user.findUnique(where)`,
  `account.create(data)`. Users get ids `u1, u2, ...`, accounts `a1, a2, ...`. Constraint errors:
  duplicate email -> `unique email`; account for a missing user -> `foreign key`.
- **Adapter** `PrismaAdapter(orm)` implements the target by translating each call.

## Input
Commands separated by `;`: `create <email> <name>`, `get <email>`, `link <userId> <provider>`.

## Output
One entry per command joined by `|`: create -> `<id>`; get -> `<id>:<name>` or `null`;
link -> `<accountId>:<userId>:<provider>`; failing command -> `ERROR:<message>` (processing continues);
unknown command -> `ERROR:unknown operation`.
