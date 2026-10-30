// Error Boundary: Shows Segment Error Boundary + Root Global Error Boundary (error.tsx / global-error.tsx).
#pragma once
#include <functional>
#include <map>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>

namespace boundary {

struct RenderError : std::runtime_error {
    using std::runtime_error::runtime_error;
};

struct Component {
    virtual ~Component() = default;
    virtual std::string render() = 0;
};

/** A component that throws for its first `fails` renders. */
class Flaky : public Component {
public:
    Flaky(int fails, std::string message, std::function<std::string()> view)
        : fails_(fails), message_(std::move(message)), view_(std::move(view)) {}
    std::string render() override {
        if (++renders_ <= fails_) throw RenderError(message_);
        return view_();
    }

private:
    int fails_, renders_ = 0;
    std::string message_;
    std::function<std::string()> view_;
};

/** Catches errors thrown by its children; errors thrown by its own fallback propagate upwards. */
class ErrorBoundary : public Component {
public:
    using Fallback = std::function<std::string(const std::string&)>;
    ErrorBoundary(Component& child, Fallback fallback) : child_(child), fallback_(std::move(fallback)) {}
    std::string render() override {
        if (!error) {
            try {
                return child_.render();
            } catch (const RenderError& e) {
                error = e.what();
            }
        }
        return fallback_(*error);
    }
    void reset() { error.reset(); }
    std::optional<std::string> error;

private:
    Component& child_;
    Fallback fallback_;
};

/** global boundary > RootLayout[header, shows boundary > page]. */
class App {
public:
    explicit App(const std::map<std::string, int>& fails)
        : page_(get(fails, "page"), "Failed to fetch shows", [] { return std::string("page"); }),
          fallbackFails_(get(fails, "fallback"), "Fallback failed", [] { return std::string(); }),
          shows(page_, [this](const std::string& e) {
              fallbackFails_.render();  // may throw -> caught by the global boundary
              return "shows-error(" + e + ")";
          }),
          layout_(get(fails, "layout"), "Root layout failed", [this] { return "root[header," + shows.render() + "]"; }),
          root(layout_, [](const std::string& e) { return "global-error(" + e + ")"; }) {}

    /** Retry button: resets the boundary showing its fallback; a reset remounts everything below it. */
    bool resetNearest() {
        if (root.error) {
            root.reset();
            shows.reset();
            return true;
        }
        if (shows.error) {
            shows.reset();
            return true;
        }
        return false;
    }

private:
    static int get(const std::map<std::string, int>& m, const std::string& k) {
        auto it = m.find(k);
        return it == m.end() ? 0 : it->second;
    }
    Flaky page_, fallbackFails_;

public:
    ErrorBoundary shows;

private:
    Flaky layout_;

public:
    ErrorBoundary root;
};

}  // namespace boundary
