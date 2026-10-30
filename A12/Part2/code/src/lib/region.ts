import { normaliseRegion } from "@/config/regions"

/** Geo headers set by common hosts (Vercel, Cloudflare), in priority order. */
export const REGION_HEADERS = ["x-vercel-ip-country", "cf-ipcountry"] as const

/** Resolve the viewer's region from request headers (CH02). */
export function regionFromHeaders(
  get: (name: string) => string | null | undefined
): string {
  for (const name of REGION_HEADERS) {
    const value = get(name)
    if (value) return normaliseRegion(value)
  }
  return normaliseRegion(null)
}
