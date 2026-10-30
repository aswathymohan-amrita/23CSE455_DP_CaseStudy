"use strict"
// Chain of Responsibility: Content Access Rule Chain (Region -> Maturity -> Premium).

const ALLOW = Object.freeze({ allowed: true })
const deny = (reason, visibility) => ({ allowed: false, reason, visibility })
const format = (d) => (d.allowed ? "ALLOW" : `DENY:${d.reason}:${d.visibility}`)

/** Handler. check() is also a template method; evaluate() is the primitive step. */
class AccessRule {
  #next = null

  setNext(rule) {
    this.#next = rule
    return rule
  }

  check(show, viewer) {
    const denial = this.evaluate(show, viewer)
    if (denial) return denial
    return this.#next ? this.#next.check(show, viewer) : ALLOW
  }

  evaluate() {
    throw new Error("abstract")
  }
}

class RegionRule extends AccessRule {
  static blocked = new Map([[550, new Set(["CN"])]])
  static allowed = new Map([[1399, new Set(["US", "GB", "IN"])]])

  evaluate(show, viewer) {
    const allowed = RegionRule.allowed.get(show.id)
    const blocked = RegionRule.blocked.get(show.id)
    const denied =
      (allowed !== undefined && !allowed.has(viewer.region)) ||
      (blocked !== undefined && blocked.has(viewer.region))
    return denied ? deny("REGION_BLOCKED", "hidden") : null
  }
}

class MaturityRule extends AccessRule {
  static policies = {
    KIDS: { allowAdult: false, blocked: new Set([27, 53, 80, 10752]) },
    TEEN: { allowAdult: false, blocked: new Set([27]) },
    ADULT: { allowAdult: true, blocked: new Set() },
    NONE: { allowAdult: true, blocked: new Set() },
  }

  evaluate(show, viewer) {
    const policy = MaturityRule.policies[viewer.maturity]
    if (!policy) throw new Error("unknown maturity")
    const denied =
      (show.adult && !policy.allowAdult) || show.genres.some((g) => policy.blocked.has(g))
    return denied ? deny("MATURITY_BLOCKED", "hidden") : null
  }
}

class PremiumContentRule extends AccessRule {
  static minTier = 3

  evaluate(show, viewer) {
    return show.premium && viewer.planTier < PremiumContentRule.minTier
      ? deny("PREMIUM_REQUIRED", "locked")
      : null
  }
}

function contentAccessChain() {
  const head = new RegionRule()
  head.setNext(new MaturityRule()).setNext(new PremiumContentRule())
  return head
}

module.exports = { AccessRule, RegionRule, MaturityRule, PremiumContentRule, contentAccessChain, format }
