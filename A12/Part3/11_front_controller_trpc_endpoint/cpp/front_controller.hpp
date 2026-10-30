// Front Controller: tRPC API Front Controller (/api/trpc/[trpc] -> createNextApiHandler -> appRouter).
#pragma once
#include <functional>
#include <map>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace fc {

struct TRPCError : std::runtime_error {
    std::string code;
    explicit TRPCError(const std::string& c) : std::runtime_error(c), code(c) {}
};

/** Request context created once per HTTP request. */
struct Context {
    std::optional<std::string> user;
    std::string db;
};

/** A command registered in the router. */
struct Procedure {
    std::function<std::string(const Context&, const std::string&)> resolver;
    bool isProtected = true;
    bool needsInput = false;
};

/** Command registry: dotted procedure path -> procedure (state after CH01). */
inline std::map<std::string, Procedure> appRouter() {
    return {
        {"user.getCurrent", {[](const Context& c, const std::string&) { return "user(" + *c.user + ")"; }}},
        {"profile.getAll", {[](const Context& c, const std::string&) { return "profiles(" + *c.user + ")"; }}},
        {"profile.getOne", {[](const Context&, const std::string& v) { return "profile(" + v + ")"; }, true, true}},
        {"icon.getAll", {[](const Context&, const std::string&) { return std::string("icons"); }, false, false}},
        {"myList.getAll", {[](const Context&, const std::string& v) {
                               if (v == "boom") throw std::logic_error("database unavailable");
                               return "list(" + v + ")";
                           }, true, true}},
        {"catalogue.checkAccess", {[](const Context&, const std::string& v) { return "access(" + v + ")"; }, true, true}},
    };
}

/** Single entry point: shared context creation, dispatch by path, one error policy. */
class FrontController {
public:
    using ContextFactory = std::function<Context(const std::optional<std::string>&)>;
    using ErrorHook = std::function<void(const std::string&, const std::string&)>;

    FrontController(std::map<std::string, Procedure> router, ContextFactory createContext, ErrorHook onError)
        : router_(std::move(router)), createContext_(std::move(createContext)), onError_(std::move(onError)) {}

    std::vector<std::string> handle(const std::optional<std::string>& user, const std::optional<std::string>& path) {
        if (!path) return {"ERROR:INTERNAL_SERVER_ERROR"};  // no [trpc] segment: nothing dispatched
        Context ctx = createContext_(user);                  // once per HTTP request, shared by a batch
        std::vector<std::string> results;
        std::stringstream ss(*path);
        std::string call;
        while (std::getline(ss, call, ',')) results.push_back(dispatch(call, ctx));
        return results;
    }

private:
    std::string dispatch(const std::string& call, const Context& ctx) {
        auto eq = call.find('=');
        std::string name = call.substr(0, eq);
        std::string value = eq == std::string::npos ? "" : call.substr(eq + 1);
        try {
            auto it = router_.find(name);
            if (it == router_.end()) throw TRPCError("NOT_FOUND");
            const Procedure& proc = it->second;
            if (proc.isProtected && !ctx.user) throw TRPCError("UNAUTHORIZED");
            if (proc.needsInput && value.empty()) throw TRPCError("BAD_REQUEST");
            return "OK:" + proc.resolver(ctx, value);
        } catch (const TRPCError& e) {
            onError_(name, e.code);
            return "ERROR:" + e.code;
        } catch (const std::exception&) {  // resolver bug -> generic server error
            onError_(name, "INTERNAL_SERVER_ERROR");
            return "ERROR:INTERNAL_SERVER_ERROR";
        }
    }

    std::map<std::string, Procedure> router_;
    ContextFactory createContext_;
    ErrorHook onError_;
};

}  // namespace fc
