package org.openwms.casestudy.ch03.repository;

import org.openwms.casestudy.ch03.domain.ReorderRequest;

import java.util.List;
import java.util.Optional;

public interface ReorderRequestRepository {

    Optional<ReorderRequest> findById(String requestId);

    Optional<ReorderRequest> findOpenByItemId(String itemId);

    List<ReorderRequest> findAll();

    void save(ReorderRequest request);
}
