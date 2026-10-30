"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { FrontController, appRouter } = require("./frontController")

function run(input) {
  const [user, path] = input.split(" ")
  const counters = { ctx: 0, logged: 0 }
  const controller = new FrontController(
    appRouter(),
    (u) => {
      counters.ctx++
      return { user: u, db: "prisma" }
    },
    () => counters.logged++
  )
  const results = controller.handle(user === "-" ? null : user, path === "-" ? null : path)
  return `${results.join("|")};ctx=${counters.ctx};logged=${counters.logged}`
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
