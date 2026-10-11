import java.util.ArrayList;
import java.util.List;

final class ObserverPattern {

    static final class Event {
        private final String type;

        Event(String type) {
            this.type = type;
        }

        String getType() {
            return type;
        }
    }

    interface Observer {
        void update(Event event);
    }

    interface EventSubject {
        void subscribe(Observer observer);

        void unsubscribe(Observer observer);

        void publish(Event event);
    }

    static final class Publisher implements EventSubject {
        private final List<Observer> observers = new ArrayList<>();

        @Override
        public void subscribe(Observer observer) {
            if (!observers.contains(observer)) {
                observers.add(observer);
            }
        }

        @Override
        public void unsubscribe(Observer observer) {
            observers.remove(observer);
        }

        @Override
        public void publish(Event event) {
            for (Observer observer : List.copyOf(observers)) {
                observer.update(event);
            }
        }
    }

    static final class RecordingObserver implements Observer {
        private final List<Event> receivedEvents = new ArrayList<>();

        @Override
        public void update(Event event) {
            receivedEvents.add(event);
        }

        List<Event> getReceivedEvents() {
            return List.copyOf(receivedEvents);
        }
    }
}
