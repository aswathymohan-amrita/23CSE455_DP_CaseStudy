// Suspense Boundary: Shows Loading Placeholder ((shows)/loading.tsx as the Suspense fallback of async pages).
#pragma once
#include <algorithm>
#include <functional>
#include <memory>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace suspense {

/** Thrown by a child that is still waiting for data (React's suspend signal). */
struct Pending {};
struct FetchError : std::runtime_error {
    using std::runtime_error::runtime_error;
};

struct Dependency {
    std::string name;
    int ms;
    bool fails;
};

struct Node {
    virtual ~Node() = default;
    virtual std::string render(int t) const = 0;
};

/** Async server page: awaits all its fetches (Promise.all) before it can render. */
class AsyncPage : public Node {
public:
    explicit AsyncPage(std::vector<Dependency> deps) : deps_(std::move(deps)) {}
    std::string render(int t) const override {
        if (std::any_of(deps_.begin(), deps_.end(), [t](const Dependency& d) { return d.ms > t; })) throw Pending{};
        auto failed = std::find_if(deps_.begin(), deps_.end(), [](const Dependency& d) { return d.fails; });
        if (failed != deps_.end()) throw FetchError(failed->name);
        return "page(rows=" + std::to_string(deps_.size()) + ")";
    }

private:
    std::vector<Dependency> deps_;
};

/** Renders the fallback while the child suspends; other errors pass through. */
class SuspenseBoundary : public Node {
public:
    SuspenseBoundary(std::shared_ptr<Node> child, std::function<std::string()> fallback)
        : child_(std::move(child)), fallback_(std::move(fallback)) {}
    std::string render(int t) const override {
        try {
            return child_->render(t);
        } catch (const Pending&) {
            return fallback_();
        }
    }

private:
    std::shared_ptr<Node> child_;
    std::function<std::string()> fallback_;
};

/** Next.js LoadingBoundary: Suspense only if the segment has loading.tsx. */
inline std::shared_ptr<Node> segment(std::shared_ptr<AsyncPage> page, bool hasLoading) {
    if (!hasLoading) return page;
    return std::make_shared<SuspenseBoundary>(page, [] { return std::string("loading"); });
}

/** Server streaming: render at every point in time where something can change; emit changed frames. */
inline std::vector<std::string> stream(const Node& root, const std::vector<Dependency>& deps) {
    std::set<int> times{0};
    for (const auto& d : deps) times.insert(d.ms);
    std::vector<std::string> frames;
    std::string last;
    for (int t : times) {
        std::string view;
        try {
            view = root.render(t);
        } catch (const Pending&) {  // no boundary: nothing can be sent yet
            continue;
        } catch (const FetchError& e) {  // handled by the segment error boundary
            view = std::string("error(") + e.what() + ")";
        }
        if (view != last) {
            frames.push_back("t=" + std::to_string(t) + ":" + view);
            last = view;
        }
        if (view != "loading") break;  // final frame sent
    }
    return frames;
}

}  // namespace suspense
