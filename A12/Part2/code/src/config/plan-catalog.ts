/**
 * Single source of truth for subscription plans (CH01 refactoring).
 *
 * Before CH01 the same plan data lived in two parallel lists: config/plans.ts (UI,
 * client-safe) and config/subscriptions.ts (server, needs Stripe price ids from the
 * env Protection Proxy, which throws when read in the browser). Adding a plan meant
 * editing both, and they had already drifted (Basic devices differed). This module
 * holds only client-safe data; both lists are now derived from it.
 */

export type PlanName = "Mobile" | "Basic" | "Standard" | "Premium" | "Ultra"
export type DeviceName = "Phone" | "Tablet" | "Computer" | "TV"

export type PlanCatalogEntry = {
  name: PlanName
  description: string
  /** Ordering used for entitlements; higher tier includes everything below. */
  tier: number
  monthlyPrice: number
  videoQuality: "Good" | "Better" | "Best"
  resolution: "480p" | "720p" | "1080p" | "4K+HDR"
  devices: DeviceName[]
  maxProfiles: number
}

/** Minimum plan tier that unlocks titles marked as premium (Netflix originals row). */
export const PREMIUM_CONTENT_MIN_TIER = 3

/** Profile limit for accounts without an active plan (baseline behaviour). */
export const DEFAULT_MAX_PROFILES = 5

const ALL_DEVICES: DeviceName[] = ["Phone", "Tablet", "Computer", "TV"]

export const planCatalog: PlanCatalogEntry[] = [
  {
    name: "Mobile",
    description: "The plan is suitable for mobile devices.",
    tier: 1,
    monthlyPrice: 2.99,
    videoQuality: "Good",
    resolution: "480p",
    devices: ["Phone", "Tablet"],
    maxProfiles: 5,
  },
  {
    name: "Basic",
    description: "The plan is suitable for basic devices.",
    tier: 2,
    monthlyPrice: 3.99,
    videoQuality: "Good",
    resolution: "720p",
    devices: ["Phone", "Tablet", "Computer"],
    maxProfiles: 5,
  },
  {
    name: "Standard",
    description: "The plan is suitable for standard devices.",
    tier: 3,
    monthlyPrice: 7.99,
    videoQuality: "Better",
    resolution: "1080p",
    devices: ALL_DEVICES,
    maxProfiles: 5,
  },
  {
    name: "Premium",
    description: "The plan is suitable for premium devices.",
    tier: 4,
    monthlyPrice: 9.99,
    videoQuality: "Best",
    resolution: "4K+HDR",
    devices: ALL_DEVICES,
    maxProfiles: 5,
  },
  {
    name: "Ultra",
    description:
      "Everything in Premium, plus up to 7 profiles for larger households.",
    tier: 5,
    monthlyPrice: 12.99,
    videoQuality: "Best",
    resolution: "4K+HDR",
    devices: ALL_DEVICES,
    maxProfiles: 7,
  },
]

export function findPlan(name: string): PlanCatalogEntry | undefined {
  return planCatalog.find((plan) => plan.name === name)
}

export function unlocksPremium(tier: number): boolean {
  return tier >= PREMIUM_CONTENT_MIN_TIER
}
