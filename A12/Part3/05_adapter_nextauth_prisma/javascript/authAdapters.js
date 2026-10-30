"use strict"
// Adapter: NextAuth Prisma Persistence Adapter.

/** Adaptee: Prisma-like client (orm.user.create({data}), orm.user.findUnique({where})). */
function createOrmClient() {
  const users = []
  const accounts = []
  const user = {
    create({ data }) {
      if (user.findUnique({ where: { email: data.email } })) throw new Error("unique email")
      const row = { id: `u${users.length + 1}`, ...data }
      users.push(row)
      return row
    },
    findUnique: ({ where }) => users.find((u) => u.email === where.email) ?? null,
  }
  const account = {
    create({ data }) {
      if (!users.some((u) => u.id === data.userId)) throw new Error("foreign key")
      const row = { id: `a${accounts.length + 1}`, ...data }
      accounts.push(row)
      return row
    },
  }
  return { user, account }
}

/** Adapter: returns an object implementing the auth library's adapter interface. */
function PrismaAdapter(p) {
  return {
    createUser: (email, name) => p.user.create({ data: { email, name } }),
    getUserByEmail: (email) => p.user.findUnique({ where: { email } }),
    linkAccount: (userId, provider) => p.account.create({ data: { userId, provider } }),
  }
}

module.exports = { createOrmClient, PrismaAdapter }
