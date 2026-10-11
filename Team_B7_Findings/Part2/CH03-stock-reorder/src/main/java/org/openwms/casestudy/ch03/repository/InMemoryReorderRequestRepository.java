package org.openwms.casestudy.ch03.repository;

import org.openwms.casestudy.ch03.domain.ReorderRequest;
import org.openwms.casestudy.ch03.domain.ReorderStatus;
import org.springframework.stereotype.Repository;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryReorderRequestRepository implements ReorderRequestRepository {

    private final Map<String, ReorderRequest> requests = new ConcurrentHashMap<>();

    @Override
    public Optional<ReorderRequest> findById(String requestId) {
        return Optional.ofNullable(requests.get(requestId));
    }

    @Override
    public Optional<ReorderRequest> findOpenByItemId(String itemId) {
        return requests.values().stream()
                .filter(request -> request.itemId().equals(itemId) && request.status() == ReorderStatus.OPEN)
                .findFirst();
    }

    @Override
    public List<ReorderRequest> findAll() {
        return requests.values().stream()
                .sorted(Comparator.comparing(ReorderRequest::id))
                .toList();
    }

    @Override
    public void save(ReorderRequest request) {
        requests.put(request.id(), request);
    }
}
