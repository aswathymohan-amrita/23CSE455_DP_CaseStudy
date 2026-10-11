package org.openwms.casestudy.ch03.repository;

import org.openwms.casestudy.ch03.domain.ReorderRule;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryReorderRuleRepository implements ReorderRuleRepository {

    private final Map<String, ReorderRule> rules = new ConcurrentHashMap<>();

    @Override
    public Optional<ReorderRule> findByItemId(String itemId) {
        return Optional.ofNullable(rules.get(itemId));
    }

    @Override
    public void save(ReorderRule rule) {
        rules.put(rule.itemId(), rule);
    }
}
