import { createTRPCRouter, subscribedProcedure } from "@/server/api/trpc"
import { TRPCError } from "@trpc/server"
import { z } from "zod"

import type { Maturity } from "@/config/maturity"
import { normaliseRegion } from "@/config/regions"
import { checkAccess } from "@/lib/access/policy"
import type { AccessContext } from "@/lib/access/types"

export const showAccessInput = z.object({
  id: z.number(),
  isPremium: z.boolean().optional(),
  // CH03: signals for parental control
  adult: z.boolean().optional(),
  genre_ids: z.array(z.number()).optional(),
  profileId: z.string().optional(),
})

export const catalogueRouter = createTRPCRouter({
  /**
   * May the current viewer play this title? First denial wins:
   * region (CH02) -> maturity of the profile (CH03) -> premium plan (CH01).
   */
  checkAccess: subscribedProcedure
    .input(showAccessInput)
    .query(async ({ ctx, input }) => {
      let maturity: Maturity | undefined
      if (input.profileId) {
        const profile = await ctx.prisma.profile.findUnique({
          where: { id: input.profileId },
          select: { userId: true, maturityLevel: true },
        })
        if (!profile || profile.userId !== ctx.session.user.id) {
          throw new TRPCError({
            code: "FORBIDDEN",
            message: "Not your profile",
          })
        }
        maturity = profile.maturityLevel
      }
      const accessCtx: AccessContext = {
        planTier: ctx.planTier,
        region: normaliseRegion(ctx.region),
        maturity,
      }
      return checkAccess(input, accessCtx)
    }),
})
