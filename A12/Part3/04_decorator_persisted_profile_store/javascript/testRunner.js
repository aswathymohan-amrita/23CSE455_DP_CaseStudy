"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { basicStore, persist, devtools } = require("./profileStores")

function run(input) {
  const [decorators, ops] = input.split(";")
  const storage = new Map()
  const log = []
  try {
    let store = basicStore()
    for (const name of decorators === "none" ? [] : decorators.split("+")) {
      if (name === "persist") store = persist(store, storage)
      else if (name === "devtools") store = devtools(store, log)
      else throw new Error(`unknown decorator ${name}`)
    }
    for (const op of ops === "-" ? [] : ops.split(",")) {
      if (op === "clear") store.clearStorage()
      else store.set(...op.split("="))
    }
    return `state=${store.state()};storage=${storage.get("test-store") ?? "-"};log=${log.join(",") || "-"}`
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
