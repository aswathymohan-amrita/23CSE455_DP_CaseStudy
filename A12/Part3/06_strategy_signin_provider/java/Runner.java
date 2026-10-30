import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] f = input.split(";");
        try {
            return new SignIn.NextAuth(List.of(f[0].split(","))).signIn(f[1], f[2]);
        } catch (IllegalArgumentException e) {
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
