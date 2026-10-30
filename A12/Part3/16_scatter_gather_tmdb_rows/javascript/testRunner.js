"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { fetchRows, sequentialCost } = require("./scatterGather")

async function run(input) {
  const rows = input === "-" ? [] : input.split(",").map((item) => {
    const [key, ms, status, count] = item.split(":")
    return { key, ms: Number(ms), ok: status === "ok", count: Number(count) }
  })
  const out = await fetchRows(rows, "Failed to fetch shows")
  const head = out.error
    ? `ERROR:${out.error}`
    : Object.entries(out.rows).map(([k, v]) => `${k}=${v}`).join(",") || "none"
  return `${head};elapsed=${out.elapsed};sequential=${sequentialCost(rows)}`
}

async function main() {
  let passed = 0
  let total = 0
  for (const line of fs.readFileSync(process.argv[2], "utf8").split("\n")) {
    if (!line.trim()) continue
    const [id, input, expected] = line.replace(/\r$/, "").split("\t")
    const got = await run(input)
    total++
    if (got === expected) passed++
    else console.log(`FAIL ${id} expected=${expected} got=${got}`)
  }
  console.log(`${passed}/${total} passed`)
  process.exit(passed === total ? 0 : 1)
}

main()
