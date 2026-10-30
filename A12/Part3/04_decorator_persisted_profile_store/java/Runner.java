import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] f = input.split(";");
        Map<String, String> storage = new HashMap<>();
        List<String> log = new ArrayList<>();
        try {
            ProfileStores.ProfileStore store = new ProfileStores.BasicStore();
            if (!f[0].equals("none")) {
                for (String name : f[0].split("\\+")) {
                    store = switch (name) {
                        case "persist" -> new ProfileStores.PersistDecorator(store, storage);
                        case "devtools" -> new ProfileStores.DevtoolsDecorator(store, log);
                        default -> throw new IllegalArgumentException("unknown decorator " + name);
                    };
                }
            }
            if (!f[1].equals("-")) {
                for (String op : f[1].split(",")) {
                    if (op.equals("clear")) store.clearStorage();
                    else store.set(op.split("=")[0], op.split("=")[1]);
                }
            }
            return "state=" + store.state() + ";storage=" + storage.getOrDefault("test-store", "-")
                    + ";log=" + (log.isEmpty() ? "-" : String.join(",", log));
        } catch (RuntimeException e) {
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
