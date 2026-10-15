#pragma once
#include <algorithm>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace diagram {
using Strings = std::vector<std::string>;
inline std::string join(const Strings& items, const std::string& separator) {
    std::string result;
    for (const auto& item : items) {
        if (!result.empty()) result += separator;
        result += item;
    }
    return result;
}
struct Block {
    virtual Strings names() const = 0;
    virtual ~Block() = default;
};
struct Node final : Block {
    std::string name;
    explicit Node(std::string name) : name(std::move(name)) {}
    Strings names() const override { return {name}; }
};
struct Group final : Block {
    std::vector<std::unique_ptr<Block>> children;
    Strings names() const override {
        Strings result;
        for (const auto& child : children) {
            auto values = child->names();
            result.insert(result.end(), values.begin(), values.end());
        }
        return result;
    }
};
struct Model {
    virtual void add(const std::string& name) = 0;
    virtual ~Model() = default;
};
struct Diagram : Model {
    Group root;
    std::vector<Group*> stack{&root};
    Strings links;
    void add(const std::string& name) override {
        auto names = root.names();
        if (std::find(names.begin(), names.end(), name) != names.end())
            throw std::invalid_argument("duplicate");
        stack.back()->children.push_back(std::make_unique<Node>(name));
    }
    void link(const std::string& left, const std::string& right) {
        auto names = root.names();
        if (std::find(names.begin(), names.end(), left) == names.end() ||
            std::find(names.begin(), names.end(), right) == names.end())
            throw std::invalid_argument("missing endpoint");
        links.push_back(left + "->" + right);
    }
};
struct Command {
    virtual void execute(Diagram& model, const Strings& args) const = 0;
    virtual ~Command() = default;
};
struct Create final : Command {
    void execute(Diagram& model, const Strings& args) const override { model.add(args[0]); }
};
struct Link final : Command {
    void execute(Diagram& model, const Strings& args) const override { model.link(args[0], args[1]); }
};
struct OpenGroup final : Command {
    void execute(Diagram& model, const Strings&) const override {
        auto group = std::make_unique<Group>();
        auto address = group.get();
        model.stack.back()->children.push_back(std::move(group));
        model.stack.push_back(address);
    }
};
struct CloseGroup final : Command {
    void execute(Diagram& model, const Strings&) const override {
        if (model.stack.size() == 1) throw std::invalid_argument("unmatched end");
        model.stack.pop_back();
    }
};
class Parser {
    std::map<std::string, std::unique_ptr<Command>> commands;
    std::map<std::string, size_t> arities{{"class",1},{"link",2},{"group",0},{"end",0}};
protected:
    virtual std::unique_ptr<Diagram> createModel() const = 0;
public:
    Parser() {
        commands["class"] = std::make_unique<Create>();
        commands["link"] = std::make_unique<Link>();
        commands["group"] = std::make_unique<OpenGroup>();
        commands["end"] = std::make_unique<CloseGroup>();
    }
    virtual ~Parser() = default;
    std::unique_ptr<Diagram> parse(const Strings& lines) const {
        auto model = createModel();
        for (const auto& line : lines) {
            std::istringstream stream(line);
            Strings words;
            std::string word;
            while (stream >> word) words.push_back(word);
            if (words.empty()) continue;
            auto found = commands.find(words[0]);
            if (found == commands.end()) throw std::invalid_argument("syntax");
            if (words.size() != arities.at(words[0]) + 1) throw std::invalid_argument("syntax");
            found->second->execute(*model, Strings(words.begin() + 1, words.end()));
        }
        if (model->stack.size() != 1) throw std::invalid_argument("unclosed group");
        return model;
    }
};
class DiagramParser final : public Parser {
    std::unique_ptr<Diagram> createModel() const override { return std::make_unique<Diagram>(); }
};
struct Renderer {
    virtual std::string render(const Diagram& model) const = 0;
    virtual ~Renderer() = default;
};
struct Compact final : Renderer {
    std::string render(const Diagram& model) const override {
        return join(model.root.names(), ",") + "|" + join(model.links, ",");
    }
};
struct Bracketed final : Renderer {
    std::string render(const Diagram& model) const override {
        auto names = model.root.names();
        for (auto& name : names) name = "[" + name + "]";
        return join(names, ",") + "|" + join(model.links, ",");
    }
};
struct LegacyNames {
    std::string encode(const Strings& names) const {
        Strings quoted;
        for (const auto& name : names) {
            std::string value = "\"";
            for (char ch : name) {
                if (ch == '\\' || ch == '"') value += '\\';
                value += ch;
            }
            quoted.push_back(value + "\"");
        }
        return "[" + join(quoted, ",") + "]";
    }
};
struct NamesAdapter final : Renderer {
    LegacyNames legacy;
    std::string render(const Diagram& model) const override { return legacy.encode(model.root.names()); }
};
struct Exporter {
    const Renderer& renderer;
    explicit Exporter(const Renderer& renderer) : renderer(renderer) {}
    std::string exportModel(const Diagram& model) const { return renderer.render(model); }
};
}
