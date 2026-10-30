// Builder: tRPC Procedure Builder (immutable fluent builder; query()/mutation() build the product).
#pragma once
#include <functional>
#include <map>
#include <optional>
#include <regex>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace builder {

struct TRPCError : std::runtime_error {
    std::string code;
    std::vector<std::string> trace;  // middlewares that ran before the call stopped
    explicit TRPCError(const std::string& c) : std::runtime_error(c), code(c) {}
};

/** Per-call state seen by middlewares and the resolver. */
struct Ctx {
    std::optional<std::string> user;
    std::optional<std::string> input;
};

using Middleware = std::pair<std::string, std::function<void(Ctx&)>>;
using Resolver = std::function<std::string(const Ctx&)>;

struct Result {
    std::string output;
    std::vector<std::string> trace;
};

/** Product: a frozen definition that can be called. */
class Procedure {
public:
    Procedure(std::string kind, std::vector<Middleware> mws, Resolver r)
        : kind_(std::move(kind)), middlewares_(std::move(mws)), resolver_(std::move(r)) {}

    Result call(std::optional<std::string> user, std::optional<std::string> input) const {
        Ctx ctx{std::move(user), std::move(input)};
        std::vector<std::string> trace;
        for (const auto& [name, fn] : middlewares_) {
            trace.push_back(name);
            try {
                fn(ctx);
            } catch (TRPCError& e) {
                e.trace = trace;
                throw;
            }
        }
        return {kind_ + ":" + resolver_(ctx), trace};
    }

private:
    std::string kind_;
    std::vector<Middleware> middlewares_;
    Resolver resolver_;
};

/** Every step returns a NEW builder; the receiver is never changed (only const member functions, no setters). */
class ProcedureBuilder {
public:
    explicit ProcedureBuilder(std::vector<Middleware> mws = {}) : middlewares_(std::move(mws)) {}

    ProcedureBuilder use(const std::string& name, std::function<void(Ctx&)> fn) const {
        auto next = middlewares_;
        next.emplace_back(name, std::move(fn));
        return ProcedureBuilder(std::move(next));
    }
    ProcedureBuilder input(std::function<void(Ctx&)> parser) const { return use("input", std::move(parser)); }
    Procedure query(Resolver r) const { return Procedure("query", middlewares_, std::move(r)); }
    Procedure mutation(Resolver r) const { return Procedure("mutation", middlewares_, std::move(r)); }
    std::size_t size() const { return middlewares_.size(); }

private:
    std::vector<Middleware> middlewares_;
};

inline void enforceUserIsAuthed(Ctx& ctx) {
    if (!ctx.user) throw TRPCError("UNAUTHORIZED");
}
inline void stringInput(Ctx& ctx) {
    if (!ctx.input) throw TRPCError("BAD_REQUEST");
}
inline void numberInput(Ctx& ctx) {
    if (!ctx.input || !std::regex_match(*ctx.input, std::regex("-?[0-9]+"))) throw TRPCError("BAD_REQUEST");
    ctx.input = std::to_string(std::stoi(*ctx.input));
}
inline void noOp(Ctx&) {}

inline const ProcedureBuilder& publicProcedure() {  // t.procedure
    static const ProcedureBuilder base;
    return base;
}
inline const ProcedureBuilder& protectedProcedure() {
    static const ProcedureBuilder p = publicProcedure().use("auth", enforceUserIsAuthed);
    return p;
}

inline Resolver resolverNamed(const std::string& name) {
    if (name == "whoami") return [](const Ctx& c) { return c.user.value_or("anonymous"); };
    return [](const Ctx& c) { return c.input.value_or("none"); };  // echo
}

/** Director: applies the step names in order to a base builder. */
inline Procedure build(const std::vector<std::string>& steps) {
    ProcedureBuilder current = steps[0] == "public" ? publicProcedure() : protectedProcedure();
    std::optional<Procedure> product;
    for (std::size_t i = 1; i < steps.size(); i++) {
        if (product) throw TRPCError("ALREADY_BUILT");
        const std::string& step = steps[i];
        auto colon = step.find(':');
        std::string kind = step.substr(0, colon), name = step.substr(colon + 1);
        if (kind == "query") product = current.query(resolverNamed(name));
        else if (kind == "mutation") product = current.mutation(resolverNamed(name));
        else if (step == "use:log") current = current.use("log", noOp);
        else if (step == "use:timing") current = current.use("timing", noOp);
        else if (step == "input:string") current = current.input(stringInput);
        else if (step == "input:number") current = current.input(numberInput);
    }
    if (!product) throw TRPCError("NOT_BUILT");
    return *product;
}

}  // namespace builder
