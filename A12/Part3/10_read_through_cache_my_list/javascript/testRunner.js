"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { createQueryCache, createMyListStore } = require("./myListCache")

function run(input) {
  const cache = createQueryCache()
  const store = createMyListStore()
  const out = []
  for (const cmd of input.split(";")) {
    const [op, profile, id] = cmd.split(" ")
    try {
      if (op === "get") out.push(`${profile}=[${cache.fetch(profile, () => store.getAll(profile)).join(",")}]`)
      else if (op === "add") store.add(profile, Number(id))
      else if (op === "remove") store.remove(profile, Number(id))
      else cache.invalidate(profile)
    } catch (e) {
      out.push(`ERROR:${e.message}`)
    }
  }
  out.push(`loads=${store.loads}`)
  return out.join("|")
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
