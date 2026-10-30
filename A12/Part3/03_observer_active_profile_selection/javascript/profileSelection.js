"use strict"
// Observer: Active Profile Selection (profile store notifies subscribed views).

const INITIAL = Object.freeze({ profile: "-", maturity: "NONE", pinForm: false })

/** ConcreteSubject: the profile store (listeners kept in an insertion-ordered Set, like zustand). */
function createProfileStore() {
  const listeners = new Set()
  let state = INITIAL
  return {
    getState: () => state,
    subscribe(listener) {
      listeners.add(listener)
      return () => listeners.delete(listener)
    },
    setState(next, out) {
      state = next
      for (const listener of listeners) {
        const reaction = listener(state)
        if (reaction !== null) out.push(reaction)
      }
    },
  }
}

// ConcreteObservers are plain functions.
const hero = (s) => `Hero:${s.maturity}`
const showsContainer = (s) => `Rows:${s.profile}/${s.maturity}`
const pinForm = (s) => (s.pinForm ? `Pin:${s.profile}` : null)

module.exports = { INITIAL, createProfileStore, hero, showsContainer, pinForm }
