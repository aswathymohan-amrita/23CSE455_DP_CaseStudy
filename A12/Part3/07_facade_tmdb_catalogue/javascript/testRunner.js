"use strict"
// Test runner: node testRunner.js ../cases.tsv
const fs = require("node:fs")
const { createTmdbCatalogue } = require("./tmdbCatalogue")

/** Test double: request n answers [n]; fails when the URL contains the fragment. */
function fakeHttp(fail) {
  const http = async (url) => {
    const n = ++http.requests
    return { ok: fail === "-" || !url.includes(fail), json: async () => ({ results: [n] }) }
  }
  http.requests = 0
  return http
}

async function run(input) {
  const cut = input.indexOf(";")
  const [mode, fail] = [input.slice(0, cut), input.slice(cut + 1)]
  const http = fakeHttp(fail)
  const facade = createTmdbCatalogue(http, "k")
  try {
    const rows = mode === "newpopular" ? await facade.getNewAndPopular() : await facade.getShows(mode)
    const parts = Object.entries(rows).map(([k, v]) => `${k}=${v[0].id}${v[0].premium ? "P" : ""}`)
    return `${parts.join(",")};requests=${http.requests}`
  } catch (e) {
    return `ERROR:${e.message};requests=${http.requests}`
  }
}

async function main() {
  let passed = 0
  let total = 0
  for (const line of fs.readFileSync(process.argv[2], "utf8").split("\n")) {
    if (!line.trim()) continue
    const [id, input, expected] = line.split("\t")
    const got = await run(input)
    total++
    if (got === expected) passed++
    else console.log(`FAIL ${id} expected=${expected} got=${got}`)
  }
  console.log(`${passed}/${total} passed`)
  process.exit(passed === total ? 0 : 1)
}

main()
