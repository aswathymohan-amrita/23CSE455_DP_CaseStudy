import type { Maturity } from "@/config/maturity"
import {
  AccessRule,
  MaturityRule,
  PremiumContentRule,
  RegionRule,
} from "./rules"
import {
  ALLOW,
  type AccessCheckedShow,
  type AccessContext,
  type AccessDecision,
} from "./types"

/** Links the rules in order and returns the head of the chain (null for no rules). */
export function buildAccessChain(rules: AccessRule[]): AccessRule | null {
  const [head, ...rest] = rules
  if (!head) return null
  rest.reduce<AccessRule>((link, rule) => link.setNext(rule), head)
  return head
}

/**
 * The rule order used by the application. Rules that hide a title run before rules
 * that only lock it, so a region-blocked premium title is hidden, not offered for
 * upgrade (CH02), and a horror title on a Kids profile is hidden (CH03).
 */
export function contentAccessChain(): AccessRule | null {
  return buildAccessChain([
    new RegionRule(),
    new MaturityRule(),
    new PremiumContentRule(),
  ])
}

export function checkAccess(
  show: AccessCheckedShow,
  ctx: AccessContext,
  chain: AccessRule | null = contentAccessChain()
): AccessDecision {
  return chain ? chain.check(show, ctx) : ALLOW
}

/** Shows that may appear in rows: allowed or merely locked (CH02). */
export function visibleShows<T extends AccessCheckedShow>(
  shows: T[],
  ctx: AccessContext,
  chain: AccessRule | null = contentAccessChain()
): T[] {
  return shows.filter((show) => {
    const decision = checkAccess(show, ctx, chain)
    return decision.allowed || decision.visibility === "locked"
  })
}

/**
 * CH03: client-side filter for the selected profile. Region was already applied on
 * the server and premium only locks, so the browser only needs the maturity link.
 */
export function profileVisibleShows<T extends AccessCheckedShow>(
  shows: T[],
  maturity: Maturity | undefined
): T[] {
  if (!maturity || maturity === "ADULT") return shows
  return visibleShows(
    shows,
    { planTier: 0, region: "", maturity },
    buildAccessChain([new MaturityRule()])
  )
}
