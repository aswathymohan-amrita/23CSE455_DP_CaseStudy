import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/** Test runner: java -cp build Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        List<ScatterGather.Row> rows = new ArrayList<>();
        if (!input.equals("-")) {
            for (String item : input.split(",")) {
                String[] f = item.split(":");
                rows.add(new ScatterGather.Row(f[0], Integer.parseInt(f[1]), f[2].equals("ok"), Integer.parseInt(f[3])));
            }
        }
        var out = ScatterGather.fetchRows(rows, "Failed to fetch shows");
        String head;
        if (out.error() != null) head = "ERROR:" + out.error();
        else if (out.rows().isEmpty()) head = "none";
        else head = out.rows().entrySet().stream().map(e -> e.getKey() + "=" + e.getValue())
                .collect(Collectors.joining(","));
        return head + ";elapsed=" + out.elapsed() + ";sequential=" + ScatterGather.sequentialCost(rows);
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
