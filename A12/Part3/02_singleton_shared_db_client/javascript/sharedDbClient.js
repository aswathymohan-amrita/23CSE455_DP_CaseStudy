"use strict"
// Singleton: Shared Prisma Database Client (globalThis holder that survives hot reloads).

const ENVS = new Set(["development", "test", "production"])

/** Process-wide state that outlives module re-evaluation (stands in for globalThis). */
function createProcessGlobals() {
  return { prisma: undefined, constructed: 0 }
}

/** Stand-in for PrismaClient; counts how many instances the process created. */
class DatabaseClient {
  constructor(processGlobals) {
    processGlobals.constructed++
  }
}

/** One evaluation of db.ts. */
function loadDbModule(globalForPrisma, nodeEnv) {
  if (!ENVS.has(nodeEnv)) throw new Error("invalid NODE_ENV")
  const prisma = globalForPrisma.prisma ?? new DatabaseClient(globalForPrisma)
  if (nodeEnv !== "production") globalForPrisma.prisma = prisma
  return { prisma }
}

module.exports = { createProcessGlobals, DatabaseClient, loadDbModule }
