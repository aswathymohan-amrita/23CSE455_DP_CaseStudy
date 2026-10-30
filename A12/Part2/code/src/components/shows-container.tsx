"use client"

import { usePathname } from "next/navigation"
import { useMounted } from "@/hooks/use-mounted"
import { useModalStore } from "@/stores/modal"
import { useProfileStore } from "@/stores/profile"
import { useSearchStore } from "@/stores/search"
import type { CategorizedShows, SessionUser, Show } from "@/types"

import { profileVisibleShows } from "@/lib/access/policy"
import { api } from "@/lib/api/api"
import { cn } from "@/lib/utils"
import ShowModal from "@/components/show-modal"
import ShowsCarousel from "@/components/shows-carousel"
import ShowsGrid from "@/components/shows-grid"
import ShowsSkeleton from "@/components/shows-skeleton"

interface ShowsContainerProps {
  user?: SessionUser
  shows: CategorizedShows[]
}

const ShowsContainer = ({ user, shows }: ShowsContainerProps) => {
  const path = usePathname()
  const mounted = useMounted()

  // stores
  const modalStore = useModalStore()
  const searchStore = useSearchStore()
  const profileStore = useProfileStore()

  // my shows query
  const myShowsQuery = profileStore.profile
    ? api.myList.getAll.useQuery(profileStore.profile.id, {
        enabled: !!user,
      })
    : null

  // CH03: hide titles the selected profile may not see
  const maturity = profileStore.profile?.maturityLevel
  const forProfile = <T extends Show>(list: T[]) =>
    profileVisibleShows(list, maturity)

  if (!mounted) return <ShowsSkeleton />

  if (searchStore.query.length > 0) {
    return <ShowsGrid shows={forProfile(searchStore.shows)} />
  }

  return (
    <div
      className={cn("w-full space-y-5 sm:space-y-10", path === "/" && "pt-24")}
    >
      {modalStore.open ? (
        <ShowModal open={modalStore.open} setOpen={modalStore.setOpen} />
      ) : null}
      {path === "/" &&
      myShowsQuery?.isSuccess &&
      myShowsQuery.data.length > 0 ? (
        <ShowsCarousel
          title="My List"
          shows={user ? forProfile(myShowsQuery.data as Show[]) : []}
        />
      ) : null}
      {shows.map((item) => (
        <ShowsCarousel
          key={item.title}
          title={item.title}
          shows={forProfile(item.shows ?? [])}
        />
      ))}
    </div>
  )
}

export default ShowsContainer
