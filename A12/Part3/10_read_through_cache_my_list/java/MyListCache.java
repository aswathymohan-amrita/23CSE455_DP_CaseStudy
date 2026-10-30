import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;

/** Read-Through Cache: My List Query Cache. */
public final class MyListCache {
    private MyListCache() {}

    /** Cache: returns the cached value or loads it once (staleTime = infinity). */
    public static final class QueryCache<K, V> {
        private final Map<K, V> entries = new HashMap<>();

        public V fetch(K key, Supplier<V> loader) {
            return entries.computeIfAbsent(key, k -> loader.get());
        }

        public void invalidate(K key) {
            entries.remove(key);
        }
    }

    /** Data source behind the loader (myList router). */
    public static final class MyListStore {
        private final Map<String, List<Integer>> lists = new HashMap<>();
        private int loads;

        public List<Integer> getAll(String profileId) {
            loads++;
            return List.copyOf(lists.getOrDefault(profileId, List.of()));
        }

        public void add(String profileId, int showId) {
            List<Integer> list = lists.computeIfAbsent(profileId, k -> new ArrayList<>());
            if (list.contains(showId)) throw new IllegalStateException("Show already exists");
            list.add(showId);
        }

        public void remove(String profileId, int showId) {
            List<Integer> list = lists.getOrDefault(profileId, new ArrayList<>());
            if (!list.remove(Integer.valueOf(showId))) throw new IllegalStateException("Show not found");
        }

        public int loads() {
            return loads;
        }
    }
}
