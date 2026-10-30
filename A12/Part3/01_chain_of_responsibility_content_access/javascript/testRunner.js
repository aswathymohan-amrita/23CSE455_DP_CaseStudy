"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { contentAccessChain, format } = require("./contentAccess")

function run(input) {
  const f = input.split(";")
  const show = {
    id: Number(f[0]),
    premium: f[1] === "1",
    adult: f[2] === "1",
    genres: f[3] === "-" ? [] : f[3].split(",").map(Number),
  }
  const viewer = { planTier: Number(f[4]), region: f[5], maturity: f[6] }
  try {
    return format(contentAccessChain().check(show, viewer))
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
