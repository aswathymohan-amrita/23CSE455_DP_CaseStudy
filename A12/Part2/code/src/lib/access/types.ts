import type { Show } from "@/types"

import type { Maturity } from "@/config/maturity"

/** What the access chain needs to know about the viewer. Built once per request. */
export interface AccessContext {
  /** 0 = no active plan; otherwise PlanCatalogEntry.tier */
  planTier: number
  /** CH02: ISO 3166-1 alpha-2 country of the viewer */
  region: string
  /** CH03: maturity of the active profile; absent = no profile chosen (ADULT) */
  maturity?: Maturity
}

/** The subset of a TMDB show the rules look at. */
export type AccessCheckedShow = Pick<Show, "id"> &
  Partial<Pick<Show, "isPremium" | "adult" | "genre_ids" | "original_language">>

export type DenialReason =
  | "PREMIUM_REQUIRED"
  | "REGION_BLOCKED"
  | "MATURITY_BLOCKED"

export type AccessDecision =
  | { allowed: true }
  | {
      allowed: false
      reason: DenialReason
      message: string
      /** "locked": show the title with an upgrade prompt; "hidden": remove it from rows */
      visibility: "locked" | "hidden"
    }

export const ALLOW: AccessDecision = { allowed: true }
