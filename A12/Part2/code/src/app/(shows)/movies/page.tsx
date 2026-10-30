import type { Metadata } from "next"

import { GENRE_ROWS, rowContext, toCategories } from "@/lib/catalogue"
import { getShows } from "@/lib/fetchers"
import { getViewerRegion } from "@/lib/server-region"
import { getCurrentUser } from "@/lib/session"
import ShowsContainer from "@/components/shows-container"

export const metadata: Metadata = {
  title: "Movies",
  description: "All movies grouped by genre",
}

export default async function MoviesPage() {
  const user = await getCurrentUser()

  const allShows = await getShows("movie")
  // CH02: hide titles not licensed in the viewer's region
  const ctx = rowContext(getViewerRegion())

  const allShowsByCategory = toCategories(allShows, GENRE_ROWS, ctx)

  return (
    <section className="pb-16 pt-10">
      <ShowsContainer user={user} shows={allShowsByCategory} />
    </section>
  )
}
