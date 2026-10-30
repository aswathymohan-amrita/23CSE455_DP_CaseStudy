import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Test runner: java Runner ../cases.tsv */
public final class Runner {
    static String run(String input) {
        var store = new ProfileSelection.ProfileStore();
        Map<String, ProfileSelection.Observer> views = Map.of(
                "Hero", new ProfileSelection.Hero(),
                "ShowsContainer", new ProfileSelection.ShowsContainer(),
                "PinForm", new ProfileSelection.PinForm());
        List<String> out = new ArrayList<>();
        for (String cmd : input.split(";")) {
            String[] p = cmd.split(" ", 2);
            switch (p[0]) {
                case "sub", "unsub" -> {
                    var view = views.get(p[1]);
                    if (view == null) return "ERROR:unknown observer";
                    if (p[0].equals("sub")) store.subscribe(view); else store.unsubscribe(view);
                }
                case "select" -> {
                    String[] s = p[1].split(":");
                    store.setState(new ProfileSelection.State(s[0], s[1], s.length > 2), out);
                }
                default -> store.setState(new ProfileSelection.State("-", "NONE", false), out);
            }
        }
        return out.isEmpty() ? "-" : String.join("|", out);
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
