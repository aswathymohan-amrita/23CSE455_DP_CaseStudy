import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/** Observer: Active Profile Selection (profile store notifies subscribed views). */
public final class ProfileSelection {
    private ProfileSelection() {}

    public record State(String profile, String maturity, boolean pinForm) {
        static final State INITIAL = new State("-", "NONE", false);
    }

    public interface Observer {
        /** Returns this observer's output for the new state, or null if it does not react. */
        String notify(State state);
    }

    /** ConcreteSubject: the profile store. */
    public static final class ProfileStore {
        private final Set<Observer> observers = new LinkedHashSet<>();
        private State state = State.INITIAL;

        public void subscribe(Observer o) {
            observers.add(o);
        }

        public void unsubscribe(Observer o) {
            observers.remove(o);
        }

        public void setState(State next, List<String> out) {
            state = next;
            for (Observer o : observers) {
                String reaction = o.notify(state);
                if (reaction != null) out.add(reaction);
            }
        }
    }

    public static final class Hero implements Observer {
        public String notify(State s) {
            return "Hero:" + s.maturity();
        }
    }

    public static final class ShowsContainer implements Observer {
        public String notify(State s) {
            return "Rows:" + s.profile() + "/" + s.maturity();
        }
    }

    public static final class PinForm implements Observer {
        public String notify(State s) {
            return s.pinForm() ? "Pin:" + s.profile() : null;
        }
    }
}
