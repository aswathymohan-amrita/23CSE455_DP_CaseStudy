#include "diagram.hpp"
#include <iostream>

int main(int argc, char** argv) {
    diagram::Strings lines;
    std::string line;
    while (std::getline(std::cin, line)) lines.push_back(line);
    try {
        auto model = diagram::DiagramParser().parse(lines);
        std::unique_ptr<diagram::Renderer> renderer;
        std::string mode = argc > 1 ? argv[1] : "compact";
        if (mode == "json") renderer = std::make_unique<diagram::NamesAdapter>();
        else if (mode == "bracketed") renderer = std::make_unique<diagram::Bracketed>();
        else renderer = std::make_unique<diagram::Compact>();
        std::cout << diagram::Exporter(*renderer).exportModel(*model) << '\n';
    } catch (const std::invalid_argument& error) {
        std::cout << "ERROR:" << error.what() << '\n';
    }
}
