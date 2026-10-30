import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    /** Test double: request n answers [n]; fails when the URL contains the fragment. */
    static final class FakeHttp implements TmdbCatalogue.HttpClient {
        final String fail;
        int requests;

        FakeHttp(String fail) {
            this.fail = fail;
        }

        public TmdbCatalogue.Response get(String url) {
            requests++;
            return new TmdbCatalogue.Response(fail.equals("-") || !url.contains(fail), List.of(requests));
        }
    }

    static String run(String input) {
        String[] f = input.split(";", 2);
        var http = new FakeHttp(f[1]);
        var facade = new TmdbCatalogue(http, "k");
        try {
            Map<String, List<TmdbCatalogue.Show>> rows =
                    f[0].equals("newpopular") ? facade.getNewAndPopular() : facade.getShows(f[0]);
            List<String> parts = new ArrayList<>();
            rows.forEach((k, v) -> parts.add(k + "=" + v.get(0).id() + (v.get(0).premium() ? "P" : "")));
            return String.join(",", parts) + ";requests=" + http.requests;
        } catch (RuntimeException e) {
            return "ERROR:" + e.getMessage() + ";requests=" + http.requests;
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
