import { createTRPCRouter, protectedProcedure } from "@/server/api/trpc"
import { MEDIA_TYPE, type PrismaClient } from "@prisma/client"
import { TRPCError } from "@trpc/server"
import { z } from "zod"

import { buildAccessChain, checkAccess } from "@/lib/access/policy"
import { MaturityRule } from "@/lib/access/rules"

/*
 * CH03 refactoring (Duplicate Code):
 * - create and update declared the same 17-field zod object twice -> showInput;
 * - create, update and delete repeated the same "load profile with list or
 *   NOT_FOUND" block -> findProfileWithList;
 * - create and update copied every field into `data` one by one -> showData.
 * Error codes/messages and stored fields are unchanged.
 */

const showInput = z.object({
  id: z.number(),
  profileId: z.string(),
  name: z.string(),
  title: z.string(),
  original_title: z.string().optional(),
  poster_path: z.string().optional(),
  backdrop_path: z.string().optional(),
  overview: z.string().optional(),
  original_language: z.string(),
  media_type: z.nativeEnum(MEDIA_TYPE),
  popularity: z.number(),
  vote_average: z.number(),
  vote_count: z.number(),
  release_date: z.string().optional(),
  first_air_date: z.string().optional(),
  adult: z.boolean().default(false),
  video: z.boolean().default(false),
  // CH03: used for the maturity check only; not stored
  genre_ids: z.array(z.number()).optional(),
})

type ShowInput = z.infer<typeof showInput>

function showData({ genre_ids: _genres, ...show }: ShowInput) {
  return show
}

async function findProfileWithList(
  prisma: Pick<PrismaClient, "profile">,
  profileId: string
) {
  const profile = await prisma.profile.findUnique({
    where: { id: profileId },
    include: { myList: true },
  })
  if (!profile) {
    throw new TRPCError({
      code: "NOT_FOUND",
      message: "Profile not found",
    })
  }
  return profile
}

function findShowOrThrow<T extends { id: number }>(list: T[], id: number) {
  const show = list.find((item) => item.id === id)
  if (!show) {
    throw new TRPCError({
      code: "NOT_FOUND",
      message: "Show not found",
    })
  }
  return show
}

export const myListRouter = createTRPCRouter({
  getAll: protectedProcedure.input(z.string()).query(async ({ ctx, input }) => {
    const shows = await ctx.prisma.myShow.findMany({
      where: { profileId: input },
    })
    return shows
  }),

  create: protectedProcedure
    .input(showInput)
    .mutation(async ({ ctx, input }) => {
      const profile = await findProfileWithList(ctx.prisma, input.profileId)

      const show = profile.myList.find((show) => show.id === input.id)

      if (show) {
        throw new TRPCError({
          code: "FORBIDDEN",
          message: "Show already exists",
        })
      }

      // CH03: a restricted profile cannot save titles it is not allowed to see
      const decision = checkAccess(
        input,
        { planTier: 0, region: "", maturity: profile.maturityLevel },
        buildAccessChain([new MaturityRule()])
      )
      if (!decision.allowed) {
        throw new TRPCError({ code: "FORBIDDEN", message: decision.message })
      }

      const createdShow = await ctx.prisma.myShow.create({
        data: showData(input),
      })
      return createdShow
    }),

  update: protectedProcedure
    .input(showInput)
    .mutation(async ({ ctx, input }) => {
      const profile = await findProfileWithList(ctx.prisma, input.profileId)
      const show = findShowOrThrow(profile.myList, input.id)

      const updatedShow = await ctx.prisma.myShow.update({
        where: { showId: show.showId },
        data: showData(input),
      })
      return updatedShow
    }),

  delete: protectedProcedure
    .input(
      z.object({
        id: z.number(),
        profileId: z.string(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const profile = await findProfileWithList(ctx.prisma, input.profileId)
      const show = findShowOrThrow(profile.myList, input.id)

      const deletedShow = await ctx.prisma.myShow.delete({
        where: { showId: show.showId },
      })
      return deletedShow
    }),
})
