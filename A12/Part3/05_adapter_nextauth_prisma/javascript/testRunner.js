"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { createOrmClient, PrismaAdapter } = require("./authAdapters")

function run(input) {
  const adapter = PrismaAdapter(createOrmClient())
  const out = []
  for (const cmd of input.split(";")) {
    const [op, a, b] = cmd.split(" ")
    try {
      if (op === "create") out.push(adapter.createUser(a, b).id)
      else if (op === "get") {
        const u = adapter.getUserByEmail(a)
        out.push(u ? `${u.id}:${u.name}` : "null")
      } else if (op === "link") {
        const acc = adapter.linkAccount(a, b)
        out.push(`${acc.id}:${acc.userId}:${acc.provider}`)
      } else out.push("ERROR:unknown operation")
    } catch (e) {
      out.push(`ERROR:${e.message}`)
    }
  }
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
