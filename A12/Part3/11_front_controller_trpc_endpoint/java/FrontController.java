import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;
import java.util.function.Function;

/** Front Controller: tRPC API Front Controller (/api/trpc/[trpc] -> createNextApiHandler -> appRouter). */
public final class FrontController {
    static final class TRPCError extends RuntimeException {
        final String code;

        TRPCError(String code) {
            super(code);
            this.code = code;
        }
    }

    /** Request context created once per HTTP request. */
    record Context(String user, String db) {}

    /** A command registered in the router. */
    record Procedure(BiFunction<Context, String, String> resolver, boolean isProtected, boolean needsInput) {}

    /** Command registry: dotted procedure path -> procedure (state after CH01). */
    static Map<String, Procedure> appRouter() {
        Map<String, Procedure> r = new LinkedHashMap<>();
        r.put("user.getCurrent", new Procedure((c, v) -> "user(" + c.user() + ")", true, false));
        r.put("profile.getAll", new Procedure((c, v) -> "profiles(" + c.user() + ")", true, false));
        r.put("profile.getOne", new Procedure((c, v) -> "profile(" + v + ")", true, true));
        r.put("icon.getAll", new Procedure((c, v) -> "icons", false, false));
        r.put("myList.getAll", new Procedure((c, v) -> {
            if (v.equals("boom")) throw new IllegalStateException("database unavailable");
            return "list(" + v + ")";
        }, true, true));
        r.put("catalogue.checkAccess", new Procedure((c, v) -> "access(" + v + ")", true, true));
        return r;
    }

    private final Map<String, Procedure> router;
    private final Function<String, Context> createContext;
    private final BiConsumer<String, String> onError;

    FrontController(Map<String, Procedure> router, Function<String, Context> createContext,
                    BiConsumer<String, String> onError) {
        this.router = router;
        this.createContext = createContext;
        this.onError = onError;
    }

    /** Single entry point: shared context creation, dispatch by path, one error policy. */
    List<String> handle(String user, String path) {
        List<String> results = new ArrayList<>();
        if (path == null) { // no [trpc] segment: nothing dispatched
            results.add("ERROR:INTERNAL_SERVER_ERROR");
            return results;
        }
        Context ctx = createContext.apply(user); // once per HTTP request, shared by a batch
        for (String call : path.split(",")) results.add(dispatch(call, ctx));
        return results;
    }

    private String dispatch(String call, Context ctx) {
        int eq = call.indexOf('=');
        String name = eq < 0 ? call : call.substring(0, eq);
        String value = eq < 0 ? "" : call.substring(eq + 1);
        try {
            Procedure proc = router.get(name);
            if (proc == null) throw new TRPCError("NOT_FOUND");
            if (proc.isProtected() && ctx.user() == null) throw new TRPCError("UNAUTHORIZED");
            if (proc.needsInput() && value.isEmpty()) throw new TRPCError("BAD_REQUEST");
            return "OK:" + proc.resolver().apply(ctx, value.isEmpty() ? null : value);
        } catch (TRPCError e) {
            onError.accept(name, e.code);
            return "ERROR:" + e.code;
        } catch (RuntimeException e) { // resolver bug -> generic server error
            onError.accept(name, "INTERNAL_SERVER_ERROR");
            return "ERROR:INTERNAL_SERVER_ERROR";
        }
    }
}
