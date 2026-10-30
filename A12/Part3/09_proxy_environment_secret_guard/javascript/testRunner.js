"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { createEnv } = require("./envGuard")

const VARS = {
  DATABASE_URL: "mysql://db",
  STRIPE_API_KEY: "sk_test_123",
  NEXT_PUBLIC_TMDB_API_KEY: "tmdb_abc",
  NEXT_PUBLIC_APP_URL: "http://localhost:3000",
}

function run(input) {
  const [side, name] = input.split(";")
  const env = createEnv(VARS, { isServer: side === "server", production: side === "client-prod" })
  try {
    return env[name] ?? "undefined"
  } catch (e) {
    return `ERROR:${e.message}`
  }
}

let passed = 0
let total = 0
for (const line of fs.readFileSync(process.argv[2], "utf8").split("\n")) {
  if (!line.trim()) continue
  const [id, input, expected] = line.split("\t")
  const got = run(input)
  total++
  if (got === expected) passed++
  else console.log(`FAIL ${id} expected=${expected} got=${got}`)
}
console.log(`${passed}/${total} passed`)
process.exit(passed === total ? 0 : 1)
