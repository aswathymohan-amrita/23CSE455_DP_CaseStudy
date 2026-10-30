import {
  createTRPCRouter,
  protectedProcedure,
  subscribedProcedure,
} from "@/server/api/trpc"
import { LANGUAGE, MATURITY } from "@prisma/client"
import { TRPCError } from "@trpc/server"
import { z } from "zod"

export const profileRouter = createTRPCRouter({
  getAll: protectedProcedure.query(async ({ ctx }) => {
    const profiles = await ctx.prisma.profile.findMany({
      where: { userId: ctx.session.user.id },
      include: {
        icon: true,
      },
    })
    return profiles
  }),

  getOthers: protectedProcedure
    .input(z.string())
    .query(async ({ ctx, input }) => {
      const profiles = await ctx.prisma.profile.findMany({
        where: { userId: ctx.session.user.id },
        include: {
          icon: true,
        },
      })
      const otherProfiles = profiles.filter((profile) => profile.id !== input)
      return otherProfiles
    }),

  getOne: protectedProcedure.input(z.string()).query(async ({ ctx, input }) => {
    const profile = await ctx.prisma.profile.findUnique({
      where: { id: input },
      include: {
        icon: true,
      },
    })
    return profile
  }),

  create: subscribedProcedure
    .input(
      z.object({
        name: z.string(),
        iconId: z.string(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      // check the profile limit of the caller's plan (5 unless the plan says otherwise)
      const profiles = await ctx.prisma.profile.findMany({
        where: { userId: ctx.session.user.id },
      })
      if (profiles.length >= ctx.maxProfiles) {
        throw new TRPCError({
          code: "FORBIDDEN",
          message: `You can only have ${ctx.maxProfiles} profiles`,
        })
      }

      // check if user has a profile with the same name
      const profileName = profiles.find(
        (profile) => profile.name === input.name
      )
      if (profileName) {
        throw new TRPCError({
          code: "FORBIDDEN",
          message: "Profile name is already taken",
        })
      }

      // check if user has a profile with the same icon
      const profileIcon = profiles.find(
        (profile) => profile.iconId === input.iconId
      )
      if (profileIcon) {
        throw new TRPCError({
          code: "FORBIDDEN",
          message: "Profile icon is already taken",
        })
      }

      const profile = await ctx.prisma.profile.create({
        data: {
          user: { connect: { id: ctx.session.user.id } },
          name: input.name,
          icon: { connect: { id: input.iconId } },
        },
      })

      return profile
    }),

  update: protectedProcedure
    .input(
      z.object({
        id: z.string(),
        name: z.string(),
        iconId: z.string(),
        language: z.nativeEnum(LANGUAGE),
        gameHandle: z.string().optional().nullable(),
        email: z.string().optional().nullable(),
        pin: z.number().optional().nullable(),
        // CH03: parental control level
        maturityLevel: z.nativeEnum(MATURITY).optional(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      // check if user has a profile with the same name
      const profileName = await ctx.prisma.profile.findFirst({
        where: { name: input.name },
      })
      if (profileName && profileName.name && profileName.id !== input.id) {
        throw new TRPCError({
          code: "FORBIDDEN",
          message: "Profile name is already taken",
        })
      }

      // check if user has a profile with the same email
      const profileEmail = await ctx.prisma.profile.findFirst({
        where: { email: input.email },
      })
      if (profileEmail && profileEmail.email && profileEmail.id !== input.id) {
        throw new TRPCError({
          code: "FORBIDDEN",
          message: "Email is already taken",
        })
      }

      // check if user has a profile with the same game handle
      const profileGameHandle = await ctx.prisma.profile.findFirst({
        where: { gameHandle: input.gameHandle },
      })
      if (
        profileGameHandle &&
        profileGameHandle.gameHandle &&
        profileGameHandle.id !== input.id
      ) {
        throw new TRPCError({
          code: "FORBIDDEN",
          message: "Game handle is already taken",
        })
      }

      const updatedProfile = await ctx.prisma.profile.update({
        where: { id: input.id },
        data: {
          name: input.name,
          icon: { connect: { id: input.iconId } },
          language: input.language,
          gameHandle: input.gameHandle,
          email: input.email,
          pin: input.pin,
          maturityLevel: input.maturityLevel,
        },
      })
      return updatedProfile
    }),

  updatePin: protectedProcedure
    .input(
      z.object({
        id: z.string(),
        pin: z
          .number()
          .refine((v) => v >= 1000 && v <= 9999)
          .optional()
          .nullable(),
        pinStatus: z.boolean(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const updatedProfile = await ctx.prisma.profile.update({
        where: { id: input.id },
        data: {
          pin: input.pinStatus ? input.pin : null,
        },
      })
      return updatedProfile
    }),

  delete: protectedProcedure
    .input(z.string())
    .mutation(async ({ ctx, input }) => {
      const profile = await ctx.prisma.profile.delete({
        where: { id: input },
      })
      return profile
    }),
})
