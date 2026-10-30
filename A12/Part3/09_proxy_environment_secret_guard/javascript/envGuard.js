"use strict"
// Proxy (protection): Environment Secret Guard - same mechanism as src/env.mjs.

function createEnv(vars, { isServer, production }) {
  return new Proxy(vars, {
    get(target, prop) {
      if (typeof prop !== "string") return undefined
      if (!isServer && !prop.startsWith("NEXT_PUBLIC_"))
        throw new Error(
          production
            ? "Attempted to access a server-side environment variable on the client"
            : `Attempted to access server-side environment variable '${prop}' on the client`
        )
      return target[prop]
    },
  })
}

module.exports = { createEnv }
