"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { AsyncPage, segment, stream } = require("./suspenseBoundary")

function run(input) {
  const [loading, spec] = input.split(" ")
  const deps = spec === "-" ? [] : spec.split(",").map((item) => {
    const [name, ms] = item.split(":")
    return { name, ms: Number(ms.replace("!", "")), fails: ms.startsWith("!") }
  })
  return stream(segment(new AsyncPage(deps), loading === "yes"), deps).join(" | ")
}

let passed = 0
let total = 0
for (const line of fs.readFileSync(process.argv[2], "utf8").split("\n")) {
  if (!line.trim()) continue
  const [id, input, expected] = line.replace(/\r$/, "").split("\t")
  const got = run(input)
  total++
  if (got === expected) passed++
  else console.log(`FAIL ${id} expected=${expected} got=${got}`)
}
console.log(`${passed}/${total} passed`)
process.exit(passed === total ? 0 : 1)
