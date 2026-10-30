/**
 * CH02: regional licensing.
 *
 * Titles are licensed per territory (ISO 3166-1 alpha-2). A licence either lists the
 * only regions where a title may be shown (allowedRegions) or the regions where it
 * may not (blockedRegions). Titles without an entry are available everywhere.
 *
 * This table is sample data keyed by TMDB id; in production it would be loaded from
 * the rights-management system.
 */
export type RegionLicence = {
  allowedRegions?: string[]
  blockedRegions?: string[]
}

export const DEFAULT_REGION = "US"

export const regionLicences: Record<number, RegionLicence> = {
  550: { blockedRegions: ["CN"] }, // Fight Club (movie)
  1399: { allowedRegions: ["US", "GB", "IN"] }, // Game of Thrones (tv)
  66732: { blockedRegions: ["RU", "BY"] }, // Stranger Things (tv)
}

/** Upper-cases a 2-letter country code; anything else falls back to DEFAULT_REGION. */
export function normaliseRegion(code?: string | null): string {
  const value = code?.trim().toUpperCase()
  return value && /^[A-Z]{2}$/.test(value) ? value : DEFAULT_REGION
}
