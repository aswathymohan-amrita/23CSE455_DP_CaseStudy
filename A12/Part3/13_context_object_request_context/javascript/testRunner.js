"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { TRPCError, call, createContext, createInnerContext } = require("./requestContext")

function run(input) {
  const [request, name] = input.split("|")
  let ctx
  if (request.startsWith("inner:")) {
    const [, user, region] = request.split(":")
    ctx = createInnerContext(user === "-" ? null : user, region === "-" ? null : region)
  } else {
    const headers = {}
    if (request !== "-") {
      for (const pair of request.split(",")) {
        const i = pair.indexOf("=")
        headers[pair.slice(0, i)] = pair.slice(i + 1)
      }
    }
    ctx = createContext(headers)
  }
  try {
    return call(name, ctx)
  } catch (e) {
    if (!(e instanceof TRPCError)) throw e
    return `ERROR:${e.code}`
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
