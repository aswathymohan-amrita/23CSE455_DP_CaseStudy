/** Send saved auth events to a listener and support unsubscribe. */
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

class AuthSubject {
  #listeners = new Set();

  subscribe(listener) {
    this.#listeners.add(listener);
    return { unsubscribe: () => this.#listeners.delete(listener) };
  }

  publish(event) {
    for (const listener of [...this.#listeners]) listener(event);
  }
}

class AuthStateObserver {
  userId = null;
  observedUsers = [];

  onAuthChange = (event) => {
    this.userId = event.event === 'SIGNED_OUT' ? null : event.user_id;
    this.observedUsers.push(this.userId);
  };
}

export function run(input) {
  if (input === null || typeof input !== 'object' || Array.isArray(input)) {
    return { error: 'input must be an object' };
  }
  if (!Array.isArray(input.events)) return { error: 'events must be an array' };
  const stop = input.unsubscribe_after ?? null;
  if (stop !== null && (!Number.isSafeInteger(stop) || stop < 0)) {
    return { error: 'unsubscribe_after must be a non-negative integer or null' };
  }
  for (const event of input.events) {
    if (event === null || typeof event !== 'object' || Array.isArray(event)) {
      return { error: 'each event must be an object' };
    }
    if (!['SIGNED_IN', 'TOKEN_REFRESHED', 'SIGNED_OUT'].includes(event.event)) {
      return { error: 'unsupported auth event' };
    }
    if (event.event === 'SIGNED_OUT') {
      if (event.user_id !== undefined && event.user_id !== null) {
        return { error: 'SIGNED_OUT user_id must be null or absent' };
      }
    } else if (typeof event.user_id !== 'string' || !event.user_id) {
      return { error: 'user_id must be a non-empty string' };
    }
  }

  const subject = new AuthSubject();
  const observer = new AuthStateObserver();
  const subscription = subject.subscribe(observer.onAuthChange);
  input.events.forEach((event, index) => {
    if (stop !== null && index === stop) subscription.unsubscribe();
    subject.publish(event);
  });
  return {
    observed_users: observer.observedUsers,
    final_user_id: observer.userId,
    notification_count: observer.observedUsers.length,
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv.length !== 3) throw new Error('usage: node implementation.mjs INPUT_JSON');
  const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
  console.log(JSON.stringify(run(input)));
}
