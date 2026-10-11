export class Event {
    constructor(type) {
        this.type = type;
        Object.freeze(this);
    }
}

export class Observer {
    update(_event) {
        throw new Error("Observer.update must be implemented");
    }
}

export class EventSubject {
    subscribe(_observer) {
        throw new Error("EventSubject.subscribe must be implemented");
    }

    unsubscribe(_observer) {
        throw new Error("EventSubject.unsubscribe must be implemented");
    }

    publish(_event) {
        throw new Error("EventSubject.publish must be implemented");
    }
}

export class Publisher extends EventSubject {
    #observers = [];

    subscribe(observer) {
        if (!this.#observers.includes(observer)) {
            this.#observers.push(observer);
        }
    }

    unsubscribe(observer) {
        this.#observers = this.#observers.filter((candidate) => candidate !== observer);
    }

    publish(event) {
        for (const observer of [...this.#observers]) {
            observer.update(event);
        }
    }
}

export class RecordingObserver extends Observer {
    receivedEvents = [];

    update(event) {
        this.receivedEvents.push(event);
    }
}
