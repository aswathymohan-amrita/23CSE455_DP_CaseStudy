import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static final Map<String, String> VARS = Map.of(
            "DATABASE_URL", "mysql://db",
            "STRIPE_API_KEY", "sk_test_123",
            "NEXT_PUBLIC_TMDB_API_KEY", "tmdb_abc",
            "NEXT_PUBLIC_APP_URL", "http://localhost:3000");

    static String run(String input) {
        String[] f = input.split(";");
        EnvGuard.Env env = EnvGuard.guard(new EnvGuard.RealEnv(VARS), f[0].equals("server"), f[0].equals("client-prod"));
        try {
            String value = env.get(f[1]);
            return value == null ? "undefined" : value;
        } catch (IllegalStateException e) {
            return "ERROR:" + e.getMessage();
        }
    }

    public static void main(String[] args) throws Exception {
        int passed = 0, total = 0;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            if (line.isBlank()) continue;
            String[] c = line.split("\t");
            String got = run(c[1]);
            total++;
            if (got.equals(c[2])) passed++;
            else System.out.println("FAIL " + c[0] + " expected=" + c[2] + " got=" + got);
        }
        System.out.println(passed + "/" + total + " passed");
        System.exit(passed == total ? 0 : 1);
    }
}
