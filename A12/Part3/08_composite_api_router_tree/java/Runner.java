import java.nio.file.Files;
import java.nio.file.Path;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        RouterTree.Router root = RouterTree.appRouter();
        String[] p = input.split(" ");
        RouterTree.Node node = p.length > 1 ? root.resolve(p[1].split("\\."), 0) : root;
        if (p[0].equals("depth")) return String.valueOf(root.depth());
        if (node == null) return "NOT_FOUND";
        return switch (p[0]) {
            case "count" -> String.valueOf(node.count());
            case "paths" -> String.join(",", RouterTree.pathsOf(node, p[1]));
            default -> node instanceof RouterTree.Procedure proc ? proc.type() : "router(" + node.count() + ")";
        };
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
