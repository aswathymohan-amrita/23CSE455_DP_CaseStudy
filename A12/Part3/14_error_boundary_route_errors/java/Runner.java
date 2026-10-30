import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Test runner: java -cp build Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] p = input.split(";");
        Map<String, Integer> fails = new HashMap<>();
        if (!p[0].equals("none")) {
            for (String pair : p[0].split(",")) {
                String[] kv = pair.split(":");
                fails.put(kv[0], Integer.parseInt(kv[1]));
            }
        }
        ErrorBoundaryApp app = new ErrorBoundaryApp(fails);
        List<String> frames = new ArrayList<>();
        frames.add(app.root.render());
        for (int i = 1; i < p.length; i++) {
            if (p[i].equals("reset") && app.resetNearest()) frames.add(app.root.render());
        }
        return String.join(" > ", frames);
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
