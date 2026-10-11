#include <cassert>
#include <memory>
#include <string>
struct Exporter {
    virtual std::string run(const std::string&)=0;
    virtual ~Exporter()=default;
};
struct Json:Exporter {
    std::string run(const std::string&s)override {
        return "{\"id\":\""+s+"\"}";
    }
};
struct Csv:Exporter {
    std::string run(const std::string&s)override {
        return s+"\n";
    }
};
struct Factory {
    virtual std::unique_ptr<Exporter> create()=0;
    std::string exportRecord(const std::string&s) {
        return create()->run(s);
    }
    virtual ~Factory()=default;
};
struct JsonFactory:Factory {
    std::unique_ptr<Exporter> create()override {
        return std::make_unique<Json>();
    }
};
struct CsvFactory:Factory {
    std::unique_ptr<Exporter> create()override {
        return std::make_unique<Csv>();
    }
};
int main() {
    JsonFactory j;
    CsvFactory c;
    assert(j.exportRecord("P1")=="{\"id\":\"P1\"}"&&c.exportRecord("P1")=="P1\n");
}
