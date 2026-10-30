"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { buildApp, resetNearest } = require("./errorBoundary")

function run(input) {
  const [setup, ...actions] = input.split(";")
  const fails = {}
  if (setup !== "none") {
    for (const pair of setup.split(",")) {
      const [k, v] = pair.split(":")
      fails[k] = Number(v)
    }
  }
  const app = buildApp(fails)
  const frames = [app.root.render()]
  for (const action of actions) {
    if (action === "reset" && resetNearest(app)) frames.push(app.root.render())
  }
  return frames.join(" > ")
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
