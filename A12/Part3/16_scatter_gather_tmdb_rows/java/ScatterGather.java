import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

/** Scatter-Gather: TMDB Row Scatter-Gather (Promise.all fan-out over row requests, all-or-nothing gather). */
public final class ScatterGather {
    record Row(String key, int ms, boolean ok, int count) {}

    record Response(boolean ok, int ms, List<String> results) {}

    /** rows == null means the gather failed with `error`. */
    record Outcome(Map<String, Integer> rows, String error, int elapsed) {}

    /** One TMDB endpoint; latency is simulated (reported, not slept). */
    static CompletableFuture<Response> recipient(Row row) {
        return CompletableFuture.supplyAsync(
                () -> new Response(row.ok(), row.ms(), java.util.Collections.nCopies(row.count(), "show")));
    }

    static Outcome fetchRows(List<Row> rows, String errorMessage) {
        List<CompletableFuture<Response>> futures = rows.stream().map(ScatterGather::recipient).toList(); // scatter
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        List<Response> responses = futures.stream().map(CompletableFuture::join).toList(); // request order
        int elapsed = responses.stream().mapToInt(Response::ms).max().orElse(0); // concurrent: slowest reply
        if (responses.stream().anyMatch(r -> !r.ok())) return new Outcome(null, errorMessage, elapsed);
        Map<String, Integer> out = new LinkedHashMap<>();
        for (int i = 0; i < rows.size(); i++) out.put(rows.get(i).key(), responses.get(i).results().size());
        return new Outcome(out, null, elapsed);
    }

    /** What the same requests would cost one after another. */
    static int sequentialCost(List<Row> rows) {
        return rows.stream().mapToInt(Row::ms).sum();
    }
}
