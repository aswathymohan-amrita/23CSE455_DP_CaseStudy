import { maturityPolicies, type MaturityPolicy } from "@/config/maturity"
import { PREMIUM_CONTENT_MIN_TIER } from "@/config/plan-catalog"
import { regionLicences, type RegionLicence } from "@/config/regions"
import {
  ALLOW,
  type AccessCheckedShow,
  type AccessContext,
  type AccessDecision,
} from "./types"

/**
 * Chain of Responsibility: each rule either denies access (and stops the chain) or
 * passes the request to the next rule. A chain with no denial allows the title.
 */
export abstract class AccessRule {
  private next: AccessRule | null = null

  /** Links `rule` after this one and returns it, so links can be chained. */
  setNext(rule: AccessRule): AccessRule {
    this.next = rule
    return rule
  }

  check(show: AccessCheckedShow, ctx: AccessContext): AccessDecision {
    const denial = this.evaluate(show, ctx)
    if (denial) return denial
    return this.next ? this.next.check(show, ctx) : ALLOW
  }

  /** Return a denial, or null to pass the request on. */
  protected abstract evaluate(
    show: AccessCheckedShow,
    ctx: AccessContext
  ): AccessDecision | null
}

/** CH01: premium titles need a plan whose tier unlocks premium content. */
export class PremiumContentRule extends AccessRule {
  constructor(private readonly minTier: number = PREMIUM_CONTENT_MIN_TIER) {
    super()
  }

  protected evaluate(
    show: AccessCheckedShow,
    ctx: AccessContext
  ): AccessDecision | null {
    if (!show.isPremium || ctx.planTier >= this.minTier) return null
    return {
      allowed: false,
      reason: "PREMIUM_REQUIRED",
      message: "This title is included with Standard, Premium and Ultra plans.",
      visibility: "locked",
    }
  }
}

/** CH02: titles not licensed in the viewer's region are hidden. */
export class RegionRule extends AccessRule {
  constructor(
    private readonly licences: Record<number, RegionLicence> = regionLicences
  ) {
    super()
  }

  protected evaluate(
    show: AccessCheckedShow,
    ctx: AccessContext
  ): AccessDecision | null {
    const licence = this.licences[show.id]
    if (!licence) return null
    const notAllowed =
      licence.allowedRegions !== undefined &&
      !licence.allowedRegions.includes(ctx.region)
    const blocked = licence.blockedRegions?.includes(ctx.region) ?? false
    if (!notAllowed && !blocked) return null
    return {
      allowed: false,
      reason: "REGION_BLOCKED",
      message: "This title is not available in your region.",
      visibility: "hidden",
    }
  }
}

/** CH03: titles unsuitable for the active profile's maturity level are hidden. */
export class MaturityRule extends AccessRule {
  constructor(
    private readonly policies: Record<string, MaturityPolicy> = maturityPolicies
  ) {
    super()
  }

  protected evaluate(
    show: AccessCheckedShow,
    ctx: AccessContext
  ): AccessDecision | null {
    const policy = this.policies[ctx.maturity ?? "ADULT"]
    if (!policy) return null
    const adultBlocked = !!show.adult && !policy.allowAdult
    const genreBlocked = (show.genre_ids ?? []).some((id) =>
      policy.blockedGenres.includes(id)
    )
    if (!adultBlocked && !genreBlocked) return null
    return {
      allowed: false,
      reason: "MATURITY_BLOCKED",
      message: "This title is not available on this profile.",
      visibility: "hidden",
    }
  }
}
