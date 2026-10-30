"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { createProcessGlobals, loadDbModule } = require("./sharedDbClient")

function run(input) {
  const [env, ops] = input.split(";")
  const globals = createProcessGlobals()
  const seen = new Set()
  try {
    let mod = loadDbModule(globals, env)
    for (const op of ops === "-" ? [] : ops.split(",")) {
      if (op === "reload") mod = loadDbModule(globals, env)
      else seen.add(mod.prisma)
    }
  } catch (e) {
    return `ERROR:${e.message}`
  }
  return `constructed=${globals.constructed};distinct=${seen.size}`
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
