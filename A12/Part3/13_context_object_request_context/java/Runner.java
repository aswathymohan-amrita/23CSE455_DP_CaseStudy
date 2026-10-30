import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

/** Test runner: java -cp build Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] p = input.split("\\|");
        RequestContext.Ctx ctx;
        if (p[0].startsWith("inner:")) {
            String[] q = p[0].split(":");
            ctx = RequestContext.createInnerContext(q[1].equals("-") ? null : q[1], q[2].equals("-") ? null : q[2]);
        } else {
            Map<String, String> headers = new HashMap<>();
            if (!p[0].equals("-")) {
                for (String pair : p[0].split(",")) {
                    int i = pair.indexOf('=');
                    headers.put(pair.substring(0, i), pair.substring(i + 1));
                }
            }
            ctx = RequestContext.createContext(headers);
        }
        try {
            return RequestContext.call(p[1], ctx);
        } catch (RequestContext.TRPCError e) {
            return "ERROR:" + e.code;
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
