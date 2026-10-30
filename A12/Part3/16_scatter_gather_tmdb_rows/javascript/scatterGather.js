"use strict"
// Scatter-Gather: TMDB Row Scatter-Gather (Promise.all fan-out over row requests, all-or-nothing gather).

/** One TMDB endpoint; latency is simulated (reported, not slept). */
const recipient = async (row) => ({ ok: row.ok, ms: row.ms, results: Array(row.count).fill("show") })

async function fetchRows(rows, errorMessage) {
  const responses = await Promise.all(rows.map(recipient)) // scatter, keeps request order
  const elapsed = Math.max(0, ...responses.map((r) => r.ms)) // concurrent: slowest reply
  if (responses.some((r) => !r.ok)) return { error: errorMessage, elapsed } // completeness rule
  return { rows: Object.fromEntries(rows.map((row, i) => [row.key, responses[i].results.length])), elapsed }
}

/** What the same requests would cost one after another. */
const sequentialCost = (rows) => rows.reduce((sum, r) => sum + r.ms, 0)

module.exports = { fetchRows, sequentialCost }
