import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        String[] f = input.split(";");
        Set<Integer> genres = f[3].equals("-") ? Set.of()
                : Arrays.stream(f[3].split(",")).map(Integer::parseInt).collect(Collectors.toSet());
        var show = new ContentAccess.Show(Integer.parseInt(f[0]), f[1].equals("1"), f[2].equals("1"), genres);
        var viewer = new ContentAccess.Viewer(Integer.parseInt(f[4]), f[5], f[6]);
        try {
            return ContentAccess.contentAccessChain().check(show, viewer).toString();
        } catch (IllegalArgumentException e) {
            return "ERROR:" + e.getMessage();
        }
    }

    public static void main(String[] args) throws Exception {
        List<String> lines = Files.readAllLines(Path.of(args[0]));
        int passed = 0, total = 0;
        for (String line : lines) {
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
