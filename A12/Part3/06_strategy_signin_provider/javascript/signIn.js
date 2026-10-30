"use strict"
// Strategy: Sign-in Provider Strategy (NextAuth providers as config objects).

const GoogleProvider = () => ({
  id: "google",
  authorize: (c) => (c.startsWith("g-") ? `google:${c.slice(2)}` : null),
})

const GithubProvider = () => ({
  id: "github",
  authorize: (c) => (c.startsWith("gh-") ? `github:${c.slice(3)}` : null),
})

const EmailProvider = () => ({
  id: "email",
  authorize: (c) => (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(c) ? `email:${c.toLowerCase()}` : null),
})

const registry = { google: GoogleProvider, github: GithubProvider, email: EmailProvider }

/** Context: keeps the configured strategies and delegates to the selected one. */
function NextAuth(providerIds) {
  const providers = new Map()
  for (const id of providerIds) {
    const factory = registry[id]
    if (!factory) throw new Error(`unsupported provider ${id}`)
    providers.set(id, factory())
  }
  return {
    signIn(providerId, credential) {
      const provider = providers.get(providerId)
      if (!provider) return "ERR:unknown provider"
      const profile = provider.authorize(credential)
      return profile ? `OK:${profile}` : "ERR:invalid credentials"
    },
  }
}

module.exports = { GoogleProvider, GithubProvider, EmailProvider, NextAuth }
