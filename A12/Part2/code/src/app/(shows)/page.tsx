import { visibleShows } from "@/lib/access/policy"
import { GENRE_ROWS, rowContext, toCategories } from "@/lib/catalogue"
import { getShows } from "@/lib/fetchers"
import { getViewerRegion } from "@/lib/server-region"
import { getCurrentUser } from "@/lib/session"
import Hero from "@/components/hero"
import ShowsContainer from "@/components/shows-container"

export default async function Home() {
  const user = await getCurrentUser()

  const allShows = await getShows("movie")
  // CH02: hide titles not licensed in the viewer's region
  const ctx = rowContext(getViewerRegion())

  const allShowsByCategory = toCategories(allShows, GENRE_ROWS, ctx)

  return (
    <section>
      <div className="pb-16 pt-10">
        <Hero shows={visibleShows(allShows.netflix ?? [], ctx)} />
        <ShowsContainer user={user} shows={allShowsByCategory} />
      </div>
    </section>
  )
}
