import { vi } from "vitest"

/** In-memory stand-in for the parts of PrismaClient the routers use. */
export function fakePrisma(overrides: Record<string, unknown> = {}) {
  return {
    profile: {
      findMany: vi.fn().mockResolvedValue([]),
      findUnique: vi.fn().mockResolvedValue(null),
      findFirst: vi.fn().mockResolvedValue(null),
      create: vi.fn(async ({ data }: { data: unknown }) => ({
        id: "new",
        ...(data as object),
      })),
      update: vi.fn(async ({ data }: { data: unknown }) => data),
      delete: vi.fn(),
    },
    user: {
      findUnique: vi.fn().mockResolvedValue(null),
      // CH01: a signed-in user always has a User row; default = no subscription
      findFirst: vi.fn().mockResolvedValue({ stripeSubscriptionId: null }),
      update: vi.fn(),
    },
    myShow: {
      findMany: vi.fn().mockResolvedValue([]),
      create: vi.fn(async ({ data }: { data: unknown }) => data),
      update: vi.fn(),
      delete: vi.fn(),
    },
    icon: { findMany: vi.fn().mockResolvedValue([]) },
    ...overrides,
  }
}

export const session = (id = "user_1") => ({
  user: { id, name: "Test", email: "t@example.com" },
  expires: "2999-01-01",
})

/** Records the URLs passed to fetch and answers each with {results:[{id: n}]} */
export function mockFetch(fail = false) {
  const urls: string[] = []
  const fn = vi.fn(async (url: string) => {
    urls.push(url)
    const n = urls.length
    return {
      ok: !fail,
      json: async () => ({ results: [{ id: n, popularity: n }] }),
    }
  })
  vi.stubGlobal("fetch", fn)
  return urls
}
