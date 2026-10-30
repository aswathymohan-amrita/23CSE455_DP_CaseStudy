// Context Object: tRPC Request Context (createTRPCContext -> createInnerTRPCContext -> middleware refinement).
#pragma once
#include <algorithm>
#include <cctype>
#include <functional>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

namespace reqctx {

const std::string DEFAULT_REGION = "US";
const std::vector<std::string> REGION_HEADERS = {"x-vercel-ip-country", "cf-ipcountry"};
const int DEFAULT_MAX_PROFILES = 5;

struct Plan {
    std::string name;
    int tier;
    int maxProfiles;
};

inline const std::map<std::string, Plan>& plans() {  // fake database
    static const std::map<std::string, Plan> db = {{"u1", {"Premium", 3, 5}}, {"u2", {"Mobile", 1, 2}}};
    return db;
}

struct TRPCError : std::runtime_error {
    std::string code;
    explicit TRPCError(const std::string& c) : std::runtime_error(c), code(c) {}
};

/** The context object: key -> value (std::map keeps keys sorted). Middlewares return refined copies. */
using Ctx = std::map<std::string, std::string>;

inline std::string normaliseRegion(const std::optional<std::string>& code) {
    std::string v = code.value_or("");
    auto b = v.find_first_not_of(" \t"), e = v.find_last_not_of(" \t");
    v = b == std::string::npos ? "" : v.substr(b, e - b + 1);
    std::transform(v.begin(), v.end(), v.begin(), [](unsigned char c) { return std::toupper(c); });
    bool ok = v.size() == 2 && std::isupper(static_cast<unsigned char>(v[0])) && std::isupper(static_cast<unsigned char>(v[1]));
    return ok ? v : DEFAULT_REGION;
}

inline std::string regionFromHeaders(const std::map<std::string, std::string>& headers) {
    for (const auto& name : REGION_HEADERS) {
        auto it = headers.find(name);
        if (it != headers.end() && !it->second.empty()) return normaliseRegion(it->second);
    }
    return normaliseRegion(std::nullopt);
}

/** Protocol-independent context (also used by tests without HTTP). "" stands for a missing session. */
inline Ctx createInnerContext(const std::optional<std::string>& session, const std::optional<std::string>& region) {
    return {{"session", session.value_or("")}, {"db", "prisma"}, {"region", normaliseRegion(region)}};
}

/** Per-request factory: extracts session and region from the HTTP request once. */
inline Ctx createContext(const std::map<std::string, std::string>& headers) {
    auto it = headers.find("session");
    return createInnerContext(it == headers.end() ? std::nullopt : std::optional<std::string>(it->second),
                              regionFromHeaders(headers));
}

inline Ctx enforceUserIsAuthed(Ctx ctx) {  // takes a copy: the caller's context is untouched
    if (ctx["session"].empty()) throw TRPCError("UNAUTHORIZED");
    return ctx;
}

inline Ctx attachSubscription(Ctx ctx) {
    auto it = plans().find(ctx["session"]);
    bool has = it != plans().end();
    ctx["subscription"] = has ? it->second.name : "";
    ctx["planTier"] = std::to_string(has ? it->second.tier : 0);
    ctx["maxProfiles"] = std::to_string(has ? it->second.maxProfiles : DEFAULT_MAX_PROFILES);
    return ctx;
}

struct Proc {
    std::vector<std::function<Ctx(Ctx)>> middlewares;
    std::function<std::string(const Ctx&)> resolver;
};

inline std::string call(const std::string& name, Ctx ctx) {
    static const std::map<std::string, Proc> procedures = {
        {"whoami", {{enforceUserIsAuthed}, [](const Ctx& c) { return c.at("session"); }}},
        {"region", {{}, [](const Ctx& c) { return c.at("region"); }}},
        {"plan", {{enforceUserIsAuthed, attachSubscription},
                  [](const Ctx& c) { return "tier=" + c.at("planTier") + ",max=" + c.at("maxProfiles"); }}},
    };
    const Proc& proc = procedures.at(name);
    for (const auto& mw : proc.middlewares) ctx = mw(ctx);
    std::string keys;
    for (const auto& [k, v] : ctx) keys += (keys.empty() ? "" : ",") + k;
    return proc.resolver(ctx) + ";keys=" + keys;
}

}  // namespace reqctx
