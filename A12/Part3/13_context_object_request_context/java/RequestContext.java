import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.function.Function;
import java.util.function.UnaryOperator;

/** Context Object: tRPC Request Context (createTRPCContext -> createInnerTRPCContext -> middleware refinement). */
public final class RequestContext {
    static final String DEFAULT_REGION = "US";
    static final List<String> REGION_HEADERS = List.of("x-vercel-ip-country", "cf-ipcountry");
    static final int DEFAULT_MAX_PROFILES = 5;

    record Plan(String name, int tier, int maxProfiles) {}

    static final Map<String, Plan> PLANS = Map.of( // fake database
            "u1", new Plan("Premium", 3, 5),
            "u2", new Plan("Mobile", 1, 2));

    static final class TRPCError extends RuntimeException {
        final String code;

        TRPCError(String code) {
            super(code);
            this.code = code;
        }
    }

    /** The context object: an immutable key -> value map handed to every middleware and resolver. */
    record Ctx(Map<String, Object> values) {
        Object get(String key) {
            return values.get(key);
        }

        Ctx with(Map<String, Object> additions) { // refined copy, original untouched
            Map<String, Object> next = new TreeMap<>(values);
            next.putAll(additions);
            return new Ctx(Collections.unmodifiableMap(next));
        }
    }

    static String normaliseRegion(String code) {
        String value = code == null ? "" : code.strip().toUpperCase();
        return value.matches("[A-Z]{2}") ? value : DEFAULT_REGION;
    }

    static String regionFromHeaders(Map<String, String> headers) {
        for (String name : REGION_HEADERS) {
            String value = headers.get(name);
            if (value != null && !value.isEmpty()) return normaliseRegion(value);
        }
        return normaliseRegion(null);
    }

    /** Protocol-independent context (also used by tests without HTTP). */
    static Ctx createInnerContext(String session, String region) {
        Map<String, Object> m = new TreeMap<>();
        m.put("session", session);
        m.put("db", PLANS);
        m.put("region", normaliseRegion(region));
        return new Ctx(Collections.unmodifiableMap(m));
    }

    /** Per-request factory: extracts session and region from the HTTP request once. */
    static Ctx createContext(Map<String, String> headers) {
        return createInnerContext(headers.get("session"), regionFromHeaders(headers));
    }

    static Ctx enforceUserIsAuthed(Ctx ctx) {
        if (ctx.get("session") == null) throw new TRPCError("UNAUTHORIZED");
        return ctx.with(Map.of("session", ctx.get("session")));
    }

    @SuppressWarnings("unchecked")
    static Ctx attachSubscription(Ctx ctx) {
        Plan plan = ((Map<String, Plan>) ctx.get("db")).get((String) ctx.get("session"));
        Map<String, Object> add = new TreeMap<>();
        add.put("subscription", plan == null ? null : plan.name());
        add.put("planTier", plan == null ? 0 : plan.tier());
        add.put("maxProfiles", plan == null ? DEFAULT_MAX_PROFILES : plan.maxProfiles());
        return ctx.with(add);
    }

    record Proc(List<UnaryOperator<Ctx>> middlewares, Function<Ctx, String> resolver) {}

    static final Map<String, Proc> PROCEDURES = Map.of(
            "whoami", new Proc(List.of(RequestContext::enforceUserIsAuthed), c -> (String) c.get("session")),
            "region", new Proc(List.of(), c -> (String) c.get("region")),
            "plan", new Proc(List.of(RequestContext::enforceUserIsAuthed, RequestContext::attachSubscription),
                    c -> "tier=" + c.get("planTier") + ",max=" + c.get("maxProfiles")));

    static String call(String name, Ctx ctx) {
        Proc proc = PROCEDURES.get(name);
        for (UnaryOperator<Ctx> mw : proc.middlewares()) ctx = mw.apply(ctx);
        return proc.resolver().apply(ctx) + ";keys=" + String.join(",", new ArrayList<>(ctx.values().keySet()));
    }
}
