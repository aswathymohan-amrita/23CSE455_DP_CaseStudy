// Singleton: Shared Prisma Database Client (globalThis holder that survives hot reloads).
#pragma once
#include <memory>
#include <set>
#include <stdexcept>
#include <string>

namespace db {

struct ProcessGlobals;

// Stand-in for PrismaClient; counts how many instances the process created.
class DatabaseClient {
public:
    explicit DatabaseClient(ProcessGlobals& process);
};

// Process-wide state that outlives module re-evaluation (globalThis).
struct ProcessGlobals {
    std::shared_ptr<DatabaseClient> prisma;
    int constructed = 0;
};

inline DatabaseClient::DatabaseClient(ProcessGlobals& process) { process.constructed++; }

// One evaluation of db.ts.
class DbModule {
public:
    DbModule(ProcessGlobals& process, const std::string& nodeEnv) {
        static const std::set<std::string> envs{"development", "test", "production"};
        if (!envs.count(nodeEnv)) throw std::invalid_argument("invalid NODE_ENV");
        prisma_ = process.prisma ? process.prisma : std::make_shared<DatabaseClient>(process);
        if (nodeEnv != "production") process.prisma = prisma_;
    }
    std::shared_ptr<DatabaseClient> prisma() const { return prisma_; }

private:
    std::shared_ptr<DatabaseClient> prisma_;
};

}  // namespace db
