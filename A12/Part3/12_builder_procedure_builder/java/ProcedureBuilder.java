import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.UnaryOperator;

/** Builder: tRPC Procedure Builder (immutable fluent builder; query()/mutation() build the product). */
public final class ProcedureBuilder {
    static final class TRPCError extends RuntimeException {
        final String code;
        List<String> trace = List.of(); // middlewares that ran before the call stopped

        TRPCError(String code) {
            super(code);
            this.code = code;
        }
    }

    /** Mutable per-call state seen by middlewares and the resolver. */
    static final class Ctx {
        final String user;
        String input;

        Ctx(String user, String input) {
            this.user = user;
            this.input = input;
        }
    }

    record Middleware(String name, Consumer<Ctx> fn) {}

    record Result(String output, List<String> trace) {}

    /** Product: a frozen definition that can be called. */
    record Procedure(String kind, List<Middleware> middlewares, Function<Ctx, String> resolver) {
        Result call(String user, String input) {
            Ctx ctx = new Ctx(user, input);
            List<String> trace = new ArrayList<>();
            for (Middleware mw : middlewares) {
                trace.add(mw.name());
                try {
                    mw.fn().accept(ctx);
                } catch (TRPCError e) {
                    e.trace = trace;
                    throw e;
                }
            }
            return new Result(kind + ":" + resolver.apply(ctx), trace);
        }
    }

    final List<Middleware> middlewares; // immutable

    ProcedureBuilder(List<Middleware> middlewares) {
        this.middlewares = List.copyOf(middlewares);
    }

    /** Every step returns a NEW builder; the receiver is never changed. */
    ProcedureBuilder use(String name, Consumer<Ctx> fn) {
        List<Middleware> next = new ArrayList<>(middlewares);
        next.add(new Middleware(name, fn));
        return new ProcedureBuilder(next);
    }

    ProcedureBuilder input(Consumer<Ctx> parser) {
        return use("input", parser);
    }

    Procedure query(Function<Ctx, String> resolver) {
        return new Procedure("query", middlewares, resolver);
    }

    Procedure mutation(Function<Ctx, String> resolver) {
        return new Procedure("mutation", middlewares, resolver);
    }

    static void enforceUserIsAuthed(Ctx ctx) {
        if (ctx.user == null) throw new TRPCError("UNAUTHORIZED");
    }

    static void stringInput(Ctx ctx) {
        if (ctx.input == null) throw new TRPCError("BAD_REQUEST");
    }

    static void numberInput(Ctx ctx) {
        if (ctx.input == null || !ctx.input.matches("-?\\d+")) throw new TRPCError("BAD_REQUEST");
        ctx.input = String.valueOf(Integer.parseInt(ctx.input));
    }

    static void noOp(Ctx ctx) {}

    static final ProcedureBuilder PUBLIC = new ProcedureBuilder(List.of()); // t.procedure
    static final ProcedureBuilder PROTECTED = PUBLIC.use("auth", ProcedureBuilder::enforceUserIsAuthed);
    static final Map<String, Function<Ctx, String>> RESOLVERS = Map.of(
            "echo", ctx -> ctx.input != null ? ctx.input : "none",
            "whoami", ctx -> ctx.user != null ? ctx.user : "anonymous");
    static final Map<String, UnaryOperator<ProcedureBuilder>> STEPS = Map.of(
            "use:log", b -> b.use("log", ProcedureBuilder::noOp),
            "use:timing", b -> b.use("timing", ProcedureBuilder::noOp),
            "input:string", b -> b.input(ProcedureBuilder::stringInput),
            "input:number", b -> b.input(ProcedureBuilder::numberInput));

    /** Director: applies the step names in order to a base builder. */
    static Procedure build(String[] steps) {
        ProcedureBuilder builder = steps[0].equals("public") ? PUBLIC : PROTECTED;
        Procedure product = null;
        for (int i = 1; i < steps.length; i++) {
            if (product != null) throw new TRPCError("ALREADY_BUILT");
            String[] kn = steps[i].split(":");
            if (kn[0].equals("query")) product = builder.query(RESOLVERS.get(kn[1]));
            else if (kn[0].equals("mutation")) product = builder.mutation(RESOLVERS.get(kn[1]));
            else builder = STEPS.get(steps[i]).apply(builder);
        }
        if (product == null) throw new TRPCError("NOT_BUILT");
        return product;
    }
}
