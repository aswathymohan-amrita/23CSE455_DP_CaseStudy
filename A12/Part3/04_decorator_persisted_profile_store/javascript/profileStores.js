"use strict"
// Decorator: Persisted Profile Store (devtools(persist(creator))), zustand-style functions.

/** ConcreteComponent. */
function basicStore() {
  const fields = { profile: "null", pinForm: "false" }
  return {
    set(field, value) {
      if (!(field in fields)) throw new Error(`unknown field ${field}`)
      fields[field] = value
    },
    state: () => `profile=${fields.profile}&pinForm=${fields.pinForm}`,
    clearStorage() {
      throw new Error("clearStorage not available")
    },
  }
}

/** Decorator: same shape as the store it wraps, plus persistence. */
function persist(inner, storage, key = "test-store") {
  return {
    ...inner,
    set(field, value) {
      inner.set(field, value)
      storage.set(key, inner.state())
    },
    clearStorage: () => storage.delete(key),
  }
}

/** Decorator: logs every successful set. */
function devtools(inner, log) {
  return {
    ...inner,
    set(field, value) {
      inner.set(field, value)
      log.push(`set ${field}=${value}`)
    },
  }
}

module.exports = { basicStore, persist, devtools }
