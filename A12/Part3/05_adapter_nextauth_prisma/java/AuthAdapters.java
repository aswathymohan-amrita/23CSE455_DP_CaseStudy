import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/** Adapter: NextAuth Prisma Persistence Adapter. */
public final class AuthAdapters {
    private AuthAdapters() {}

    public record User(String id, String email, String name) {}

    public record Account(String id, String userId, String provider) {}

    /** Target: what the auth library calls. */
    public interface AuthAdapter {
        User createUser(String email, String name);

        Optional<User> getUserByEmail(String email);

        Account linkAccount(String userId, String provider);
    }

    /** Adaptee: Prisma-like client with a different interface (data/where maps). */
    public static final class OrmClient {
        private final List<User> users = new ArrayList<>();
        private final List<Account> accounts = new ArrayList<>();

        public User userCreate(Map<String, String> data) {
            if (userFindUnique(Map.of("email", data.get("email"))) != null)
                throw new IllegalStateException("unique email");
            User u = new User("u" + (users.size() + 1), data.get("email"), data.get("name"));
            users.add(u);
            return u;
        }

        public User userFindUnique(Map<String, String> where) {
            return users.stream().filter(u -> u.email().equals(where.get("email"))).findFirst().orElse(null);
        }

        public Account accountCreate(Map<String, String> data) {
            if (users.stream().noneMatch(u -> u.id().equals(data.get("userId"))))
                throw new IllegalStateException("foreign key");
            Account a = new Account("a" + (accounts.size() + 1), data.get("userId"), data.get("provider"));
            accounts.add(a);
            return a;
        }
    }

    /** Adapter. */
    public static final class PrismaAdapter implements AuthAdapter {
        private final OrmClient orm;

        public PrismaAdapter(OrmClient orm) {
            this.orm = orm;
        }

        public User createUser(String email, String name) {
            return orm.userCreate(Map.of("email", email, "name", name));
        }

        public Optional<User> getUserByEmail(String email) {
            return Optional.ofNullable(orm.userFindUnique(Map.of("email", email)));
        }

        public Account linkAccount(String userId, String provider) {
            return orm.accountCreate(Map.of("userId", userId, "provider", provider));
        }
    }
}
