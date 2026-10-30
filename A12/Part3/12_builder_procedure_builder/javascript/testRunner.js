"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { TRPCError, build, noOp, publicProcedure, protectedProcedure } = require("./procedureBuilder")

function run(input) {
  const [chain, user, raw] = input.split(";")
  if (chain === "immutable") {
    const subscribed = protectedProcedure.use("plan", noOp)
    return `base=${publicProcedure.middlewares.length};protected=${protectedProcedure.middlewares.length};subscribed=${subscribed.middlewares.length}`
  }
  let proc
  try {
    proc = build(chain.split(","))
  } catch (e) {
    return `ERROR:${e.code}`
  }
  try {
    const { result, trace } = proc.call(user === "-" ? null : user, raw === "-" ? null : raw)
    return `${result};trace=${trace.join(">") || "none"}`
  } catch (e) {
    if (!(e instanceof TRPCError)) throw e
    return `ERROR:${e.code};trace=${e.trace.join(">")}`
  }
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
