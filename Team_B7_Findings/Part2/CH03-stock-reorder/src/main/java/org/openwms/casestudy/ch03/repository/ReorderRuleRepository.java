package org.openwms.casestudy.ch03.repository;

import org.openwms.casestudy.ch03.domain.ReorderRule;

import java.util.Optional;

public interface ReorderRuleRepository {

    Optional<ReorderRule> findByItemId(String itemId);

    void save(ReorderRule rule);
}
