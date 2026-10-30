import type { Metadata } from "next"

import {
  NEW_AND_POPULAR_LAYOUT,
  rowContext,
  toCategories,
} from "@/lib/catalogue"
import { getNewAndPopularShows } from "@/lib/fetchers"
import { getViewerRegion } from "@/lib/server-region"
import ShowsContainer from "@/components/shows-container"

export const metadata: Metadata = {
  title: "New & Popular",
  description: "All new and popular shows grouped by genre",
}

export default async function NewAndPopularPage() {
  const allShows = await getNewAndPopularShows()
  // CH02: hide titles not licensed in the viewer's region
  const ctx = rowContext(getViewerRegion())

  const allShowsByCategory = toCategories(allShows, NEW_AND_POPULAR_LAYOUT, ctx)

  return (
    <section className="pb-16 pt-10">
      <ShowsContainer shows={allShowsByCategory} />
    </section>
  )
}
