import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Test runner: java -cp build Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] p = input.split(" ");
        List<SuspenseBoundary.Dependency> deps = new ArrayList<>();
        if (!p[1].equals("-")) {
            for (String item : p[1].split(",")) {
                String[] nm = item.split(":");
                deps.add(new SuspenseBoundary.Dependency(nm[0], Integer.parseInt(nm[1].replace("!", "")),
                        nm[1].startsWith("!")));
            }
        }
        var root = SuspenseBoundary.segment(new SuspenseBoundary.AsyncPage(deps), p[0].equals("yes"));
        return String.join(" | ", SuspenseBoundary.stream(root, deps));
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
