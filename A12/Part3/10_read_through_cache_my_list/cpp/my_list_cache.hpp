// Read-Through Cache: My List Query Cache.
#pragma once
#include <algorithm>
#include <functional>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace mylist {

// Returns the cached value or loads it once (staleTime = infinity).
template <typename V>
class QueryCache {
public:
    const V& fetch(const std::string& key, const std::function<V()>& loader) {
        auto it = entries_.find(key);
        if (it == entries_.end()) it = entries_.emplace(key, loader()).first;
        return it->second;
    }
    void invalidate(const std::string& key) { entries_.erase(key); }

private:
    std::map<std::string, V> entries_;
};

// Data source behind the loader (myList router).
class MyListStore {
public:
    std::vector<int> getAll(const std::string& profileId) {
        loads++;
        auto it = lists_.find(profileId);
        return it == lists_.end() ? std::vector<int>{} : it->second;
    }
    void add(const std::string& profileId, int showId) {
        auto& list = lists_[profileId];
        if (std::find(list.begin(), list.end(), showId) != list.end()) throw std::runtime_error("Show already exists");
        list.push_back(showId);
    }
    void remove(const std::string& profileId, int showId) {
        auto& list = lists_[profileId];
        auto it = std::find(list.begin(), list.end(), showId);
        if (it == list.end()) throw std::runtime_error("Show not found");
        list.erase(it);
    }
    int loads = 0;

private:
    std::map<std::string, std::vector<int>> lists_;
};

}  // namespace mylist
