import java.nio.file.Files;
import java.nio.file.Path;

/** Test runner: java -cp build Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] p = input.split(";");
        if (p[0].equals("immutable")) {
            ProcedureBuilder subscribed = ProcedureBuilder.PROTECTED.use("plan", ProcedureBuilder::noOp);
            return "base=" + ProcedureBuilder.PUBLIC.middlewares.size() + ";protected="
                    + ProcedureBuilder.PROTECTED.middlewares.size() + ";subscribed=" + subscribed.middlewares.size();
        }
        ProcedureBuilder.Procedure proc;
        try {
            proc = ProcedureBuilder.build(p[0].split(","));
        } catch (ProcedureBuilder.TRPCError e) {
            return "ERROR:" + e.code;
        }
        try {
            var r = proc.call(p[1].equals("-") ? null : p[1], p[2].equals("-") ? null : p[2]);
            return r.output() + ";trace=" + (r.trace().isEmpty() ? "none" : String.join(">", r.trace()));
        } catch (ProcedureBuilder.TRPCError e) {
            return "ERROR:" + e.code + ";trace=" + String.join(">", e.trace);
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
