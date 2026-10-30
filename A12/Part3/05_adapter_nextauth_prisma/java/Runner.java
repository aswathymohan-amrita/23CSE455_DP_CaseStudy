import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        AuthAdapters.AuthAdapter adapter = new AuthAdapters.PrismaAdapter(new AuthAdapters.OrmClient());
        List<String> out = new ArrayList<>();
        for (String cmd : input.split(";")) {
            String[] p = cmd.split(" ");
            try {
                out.add(switch (p[0]) {
                    case "create" -> adapter.createUser(p[1], p[2]).id();
                    case "get" -> adapter.getUserByEmail(p[1]).map(u -> u.id() + ":" + u.name()).orElse("null");
                    case "link" -> {
                        var a = adapter.linkAccount(p[1], p[2]);
                        yield a.id() + ":" + a.userId() + ":" + a.provider();
                    }
                    default -> "ERROR:unknown operation";
                });
            } catch (IllegalStateException e) {
                out.add("ERROR:" + e.getMessage());
            }
        }
        return String.join("|", out);
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
