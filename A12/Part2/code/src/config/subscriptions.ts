import { env } from "@/env.mjs"
import type { SubscriptionPlan } from "@/types"

import { planCatalog, type PlanName } from "@/config/plan-catalog"

// Server-only: Stripe price ids come from secret env vars.
const stripePriceIds: Record<PlanName, string | undefined> = {
  Mobile: env.STRIPE_MOBILE_PRICE_ID,
  Basic: env.STRIPE_BASIC_PRICE_ID,
  Standard: env.STRIPE_STANDARD_PRICE_ID,
  Premium: env.STRIPE_PREMIUM_PRICE_ID,
  Ultra: env.STRIPE_ULTRA_PRICE_ID,
}

export const subscriptionPlans: SubscriptionPlan[] = planCatalog.map(
  (plan) => ({
    name: plan.name,
    description: plan.description,
    stripePriceId: stripePriceIds[plan.name] ?? "",
    monthlyPrice: plan.monthlyPrice,
    videoQuality: plan.videoQuality,
    resolution: plan.resolution,
    devices: plan.devices.join(", "),
    tier: plan.tier,
    maxProfiles: plan.maxProfiles,
  })
)
