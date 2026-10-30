/** Characterization of myList update/delete; verified against 676e5dd before CH03. */
import { describe, expect, it, vi } from "vitest"

import { fakePrisma, session } from "./helpers"

vi.mock("@/server/db", () => ({ prisma: {} }))
vi.mock("@/server/auth", () => ({ getServerAuthSession: vi.fn() }))

const show = {
  id: 42,
  profileId: "p1",
  name: "N",
  title: "T",
  original_language: "en",
  media_type: "movie" as const,
  popularity: 1,
  vote_average: 7,
  vote_count: 3,
}

async function callerWith(profile: unknown) {
  const prisma = fakePrisma()
  prisma.profile.findUnique.mockResolvedValue(profile)
  prisma.myShow.update.mockImplementation(async (args: unknown) => args)
  prisma.myShow.delete.mockImplementation(async (args: unknown) => args)
  const { appRouter } = await import("@/server/api/root")
  return {
    prisma,
    caller: appRouter.createCaller({ session: session(), prisma } as never),
  }
}

describe("myList update/delete", () => {
  it("update: unknown profile -> NOT_FOUND 'Profile not found'", async () => {
    const { caller } = await callerWith(null)
    await expect(caller.myList.update(show)).rejects.toMatchObject({
      code: "NOT_FOUND",
      message: "Profile not found",
    })
  })

  it("update: show not in list -> NOT_FOUND 'Show not found'", async () => {
    const { caller } = await callerWith({ id: "p1", myList: [] })
    await expect(caller.myList.update(show)).rejects.toMatchObject({
      code: "NOT_FOUND",
      message: "Show not found",
    })
  })

  it("update writes every field by showId", async () => {
    const { caller, prisma } = await callerWith({
      id: "p1",
      myList: [{ id: 42, showId: "s42" }],
    })
    await caller.myList.update(show)
    expect(prisma.myShow.update).toHaveBeenCalledWith({
      where: { showId: "s42" },
      data: {
        ...show,
        original_title: undefined,
        poster_path: undefined,
        backdrop_path: undefined,
        overview: undefined,
        release_date: undefined,
        first_air_date: undefined,
        adult: false,
        video: false,
      },
    })
  })

  it("delete removes by showId and reports a missing show", async () => {
    const { caller, prisma } = await callerWith({
      id: "p1",
      myList: [{ id: 42, showId: "s42" }],
    })
    await caller.myList.delete({ id: 42, profileId: "p1" })
    expect(prisma.myShow.delete).toHaveBeenCalledWith({
      where: { showId: "s42" },
    })
    await expect(
      caller.myList.delete({ id: 7, profileId: "p1" })
    ).rejects.toMatchObject({ code: "NOT_FOUND" })
  })
})
