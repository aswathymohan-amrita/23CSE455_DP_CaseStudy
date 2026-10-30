import path from "node:path"
import { defineConfig } from "vitest/config"

export default defineConfig({
  resolve: { alias: { "@": path.resolve(__dirname, "src") } },
  test: {
    environment: "node",
    include: ["tests/**/*.test.ts"],
    env: {
      SKIP_ENV_VALIDATION: "1",
      NODE_ENV: "test",
      NEXT_PUBLIC_TMDB_API_KEY: "test-key",
      STRIPE_MOBILE_PRICE_ID: "price_mobile",
      STRIPE_BASIC_PRICE_ID: "price_basic",
      STRIPE_STANDARD_PRICE_ID: "price_standard",
      STRIPE_PREMIUM_PRICE_ID: "price_premium",
    },
  },
})
