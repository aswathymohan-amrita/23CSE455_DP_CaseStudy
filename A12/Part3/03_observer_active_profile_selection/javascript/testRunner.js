"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { INITIAL, createProfileStore, hero, showsContainer, pinForm } = require("./profileSelection")

function run(input) {
  const store = createProfileStore()
  const views = { Hero: hero, ShowsContainer: showsContainer, PinForm: pinForm }
  const unsubscribe = new Map()
  const out = []
  for (const cmd of input.split(";")) {
    const [op, arg] = cmd.split(" ")
    if (op === "sub" || op === "unsub") {
      const view = views[arg]
      if (!view) return "ERROR:unknown observer"
      if (op === "sub") unsubscribe.set(view, store.subscribe(view))
      else unsubscribe.get(view)?.()
    } else if (op === "select") {
      const [profile, maturity, pin] = arg.split(":")
      store.setState({ profile, maturity, pinForm: pin !== undefined }, out)
    } else {
      store.setState(INITIAL, out)
    }
  }
  return out.length ? out.join("|") : "-"
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
