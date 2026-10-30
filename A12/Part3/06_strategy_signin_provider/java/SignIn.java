import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.function.Supplier;

/** Strategy: Sign-in Provider Strategy (NextAuth providers). */
public final class SignIn {
    private SignIn() {}

    /** Strategy. */
    public interface Provider {
        String id();

        Optional<String> authorize(String credential);
    }

    public static final class GoogleProvider implements Provider {
        public String id() {
            return "google";
        }

        public Optional<String> authorize(String c) {
            return c.startsWith("g-") ? Optional.of("google:" + c.substring(2)) : Optional.empty();
        }
    }

    public static final class GithubProvider implements Provider {
        public String id() {
            return "github";
        }

        public Optional<String> authorize(String c) {
            return c.startsWith("gh-") ? Optional.of("github:" + c.substring(3)) : Optional.empty();
        }
    }

    public static final class EmailProvider implements Provider {
        public String id() {
            return "email";
        }

        public Optional<String> authorize(String c) {
            return c.matches("[^@\\s]+@[^@\\s]+\\.[^@\\s]+")
                    ? Optional.of("email:" + c.toLowerCase(Locale.ROOT)) : Optional.empty();
        }
    }

    static final Map<String, Supplier<Provider>> REGISTRY = Map.of(
            "google", GoogleProvider::new, "github", GithubProvider::new, "email", EmailProvider::new);

    /** Context. */
    public static final class NextAuth {
        private final Map<String, Provider> providers = new LinkedHashMap<>();

        public NextAuth(List<String> providerIds) {
            for (String id : providerIds) {
                Supplier<Provider> factory = REGISTRY.get(id);
                if (factory == null) throw new IllegalArgumentException("unsupported provider " + id);
                providers.put(id, factory.get());
            }
        }

        public String signIn(String providerId, String credential) {
            Provider p = providers.get(providerId);
            if (p == null) return "ERR:unknown provider";
            return p.authorize(credential).map(id -> "OK:" + id).orElse("ERR:invalid credentials");
        }
    }
}
