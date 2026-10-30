/** Characterization of plan resolution (lib/subscription.ts) at the baseline. */
import { describe, expect, it, vi } from "vitest"

const findFirst = vi.fn()
vi.mock("@/server/db", () => ({ prisma: { user: { findFirst } } }))

const DAY = 86_400_000

describe("getUserSubscriptionPlan", () => {
  it("returns null without a subscription", async () => {
    findFirst.mockResolvedValue({ stripeSubscriptionId: null })
    const { getUserSubscriptionPlan } = await import("@/lib/subscription")
    expect(await getUserSubscriptionPlan("u")).toBeNull()
  })

  it("returns null when the period ended more than a day ago", async () => {
    findFirst.mockResolvedValue({
      stripeSubscriptionId: "sub",
      stripePriceId: "price_basic",
      stripeCurrentPeriodEnd: new Date(Date.now() - 2 * DAY),
      stripeCustomerId: "c",
    })
    const { getUserSubscriptionPlan } = await import("@/lib/subscription")
    expect(await getUserSubscriptionPlan("u")).toBeNull()
  })

  it("maps an active price id to its plan", async () => {
    findFirst.mockResolvedValue({
      stripeSubscriptionId: "sub",
      stripePriceId: "price_standard",
      stripeCurrentPeriodEnd: new Date(Date.now() + 10 * DAY),
      stripeCustomerId: "c",
    })
    const { getUserSubscriptionPlan } = await import("@/lib/subscription")
    const plan = await getUserSubscriptionPlan("u")
    expect(plan?.name).toBe("Standard")
    expect(plan?.resolution).toBe("1080p")
  })

  it("throws for an unknown user", async () => {
    findFirst.mockResolvedValue(null)
    const { getUserSubscriptionPlan } = await import("@/lib/subscription")
    await expect(getUserSubscriptionPlan("x")).rejects.toThrow("User not found")
  })
})
