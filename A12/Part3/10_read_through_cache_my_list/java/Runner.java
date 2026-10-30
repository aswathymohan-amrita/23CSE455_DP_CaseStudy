import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        var cache = new MyListCache.QueryCache<String, List<Integer>>();
        var store = new MyListCache.MyListStore();
        List<String> out = new ArrayList<>();
        for (String cmd : input.split(";")) {
            String[] p = cmd.split(" ");
            try {
                switch (p[0]) {
                    case "get" -> out.add(p[1] + "=" + cache.fetch(p[1], () -> store.getAll(p[1])).stream()
                            .map(String::valueOf).collect(Collectors.joining(",", "[", "]")));
                    case "add" -> store.add(p[1], Integer.parseInt(p[2]));
                    case "remove" -> store.remove(p[1], Integer.parseInt(p[2]));
                    default -> cache.invalidate(p[1]);
                }
            } catch (IllegalStateException e) {
                out.add("ERROR:" + e.getMessage());
            }
        }
        out.add("loads=" + store.loads());
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
