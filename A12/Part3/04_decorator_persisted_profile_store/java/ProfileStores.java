import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Decorator: Persisted Profile Store (devtools(persist(creator))). */
public final class ProfileStores {
    private ProfileStores() {}

    /** Component. */
    public interface ProfileStore {
        void set(String field, String value);

        String state();

        void clearStorage();
    }

    /** ConcreteComponent. */
    public static final class BasicStore implements ProfileStore {
        private final Map<String, String> fields = new LinkedHashMap<>(Map.of("profile", "null"));

        public BasicStore() {
            fields.put("pinForm", "false");
        }

        public void set(String field, String value) {
            if (!fields.containsKey(field)) throw new IllegalArgumentException("unknown field " + field);
            fields.put(field, value);
        }

        public String state() {
            return "profile=" + fields.get("profile") + "&pinForm=" + fields.get("pinForm");
        }

        public void clearStorage() {
            throw new IllegalStateException("clearStorage not available");
        }
    }

    /** Base Decorator: forwards everything to the wrapped store. */
    public abstract static class StoreDecorator implements ProfileStore {
        protected final ProfileStore inner;

        protected StoreDecorator(ProfileStore inner) {
            this.inner = inner;
        }

        public void set(String field, String value) {
            inner.set(field, value);
        }

        public String state() {
            return inner.state();
        }

        public void clearStorage() {
            inner.clearStorage();
        }
    }

    public static final class PersistDecorator extends StoreDecorator {
        static final String KEY = "test-store";
        private final Map<String, String> storage;

        public PersistDecorator(ProfileStore inner, Map<String, String> storage) {
            super(inner);
            this.storage = storage;
        }

        @Override
        public void set(String field, String value) {
            super.set(field, value);
            storage.put(KEY, state());
        }

        @Override
        public void clearStorage() {
            storage.remove(KEY);
        }
    }

    public static final class DevtoolsDecorator extends StoreDecorator {
        private final List<String> log;

        public DevtoolsDecorator(ProfileStore inner, List<String> log) {
            super(inner);
            this.log = log;
        }

        @Override
        public void set(String field, String value) {
            super.set(field, value);
            log.add("set " + field + "=" + value);
        }
    }
}
