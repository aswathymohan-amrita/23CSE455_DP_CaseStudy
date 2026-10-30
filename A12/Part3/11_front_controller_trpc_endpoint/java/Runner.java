import java.nio.file.Files;
import java.nio.file.Path;

/** Test runner: java -cp build Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] p = input.split(" ");
        int[] counters = {0, 0};
        FrontController controller = new FrontController(FrontController.appRouter(),
                u -> {
                    counters[0]++;
                    return new FrontController.Context(u, "prisma");
                },
                (path, code) -> counters[1]++);
        var results = controller.handle(p[0].equals("-") ? null : p[0], p[1].equals("-") ? null : p[1]);
        return String.join("|", results) + ";ctx=" + counters[0] + ";logged=" + counters[1];
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
