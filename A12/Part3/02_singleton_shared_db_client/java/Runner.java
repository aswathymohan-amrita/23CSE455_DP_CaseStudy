import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Set;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] f = input.split(";");
        var process = new SharedDbClient.ProcessGlobals();
        Set<Object> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        try {
            var module = new SharedDbClient.DbModule(process, f[0]);
            if (!f[1].equals("-")) {
                for (String op : f[1].split(",")) {
                    if (op.equals("reload")) module = new SharedDbClient.DbModule(process, f[0]);
                    else seen.add(module.prisma());
                }
            }
        } catch (IllegalArgumentException e) {
            return "ERROR:" + e.getMessage();
        }
        return "constructed=" + process.constructed() + ";distinct=" + seen.size();
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
