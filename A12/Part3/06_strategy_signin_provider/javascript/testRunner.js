"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { NextAuth } = require("./signIn")

function run(input) {
  const [providers, id, credential] = input.split(";")
  try {
    return NextAuth(providers.split(",")).signIn(id, credential)
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
