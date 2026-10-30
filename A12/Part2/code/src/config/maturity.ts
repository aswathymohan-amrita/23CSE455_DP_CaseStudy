/**
 * CH03: parental control.
 *
 * A profile's maturity level limits what it may see. TMDB list results give the
 * `adult` flag and `genre_ids`; these are the signals the rule uses.
 * Genre ids: 27 Horror, 53 Thriller, 80 Crime, 10752 War.
 */
export type Maturity = "KIDS" | "TEEN" | "ADULT"

export const MATURITY_LEVELS: Maturity[] = ["KIDS", "TEEN", "ADULT"]

export type MaturityPolicy = {
  allowAdult: boolean
  blockedGenres: number[]
}

export const maturityPolicies: Record<Maturity, MaturityPolicy> = {
  KIDS: { allowAdult: false, blockedGenres: [27, 53, 80, 10752] },
  TEEN: { allowAdult: false, blockedGenres: [27] },
  ADULT: { allowAdult: true, blockedGenres: [] },
}
