import { headers } from "next/headers"

import { regionFromHeaders } from "@/lib/region"

/** Viewer's region inside a server component (reads the request's geo headers). */
export function getViewerRegion(): string {
  const h = headers()
  return regionFromHeaders((name) => h.get(name))
}
