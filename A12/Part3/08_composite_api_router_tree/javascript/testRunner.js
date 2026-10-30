"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { appRouter } = require("./routerTree")

function run(input) {
  const root = appRouter()
  const [op, arg] = input.split(" ")
  if (op === "depth") return String(root.depth())
  const node = arg ? root.resolve(arg.split(".")) : root
  if (!node) return "NOT_FOUND"
  if (op === "count") return String(node.count())
  if (op === "paths") return node.paths(arg).join(",")
  return node.type ?? `router(${node.count()})`
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
