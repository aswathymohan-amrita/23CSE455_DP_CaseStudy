import type { PlansConfig } from "@/types"

import { planCatalog, type DeviceName } from "@/config/plan-catalog"
import { Icons } from "@/components/icons"

const deviceIcons: Record<
  DeviceName,
  PlansConfig["plans"][number]["devices"][number]["icon"]
> = {
  Phone: Icons.phone,
  Tablet: Icons.tablet,
  Computer: Icons.computer,
  TV: Icons.tv,
}

export const plansConfig: PlansConfig = {
  perks: [
    "Watch on your phone, tablet, laptop, and TV",
    "Unlimited movies and TV shows",
    "Change or cancel your plan anytime",
  ],
  plans: planCatalog.map((plan) => ({
    name: plan.name,
    price: plan.monthlyPrice,
    videoQuality: plan.videoQuality,
    resolution: plan.resolution,
    devices: plan.devices.map((title) => ({ title, icon: deviceIcons[title] })),
  })),
}
