package org.openwms.casestudy.ch03.controller;

import org.openwms.casestudy.ch03.exception.InsufficientStockException;
import org.openwms.casestudy.ch03.exception.InvalidReorderRuleException;
import org.openwms.casestudy.ch03.exception.InvalidReorderStatusException;
import org.openwms.casestudy.ch03.exception.InvalidStockQuantityException;
import org.openwms.casestudy.ch03.exception.ReorderRuleNotFoundException;
import org.openwms.casestudy.ch03.exception.ReorderRequestNotFoundException;
import org.openwms.casestudy.ch03.exception.StockNotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ReorderExceptionHandler {

    @ExceptionHandler({InvalidReorderRuleException.class, InvalidStockQuantityException.class})
    public ResponseEntity<ProblemDetail> handleBadRequest(RuntimeException exception) {
        return problem(HttpStatus.BAD_REQUEST, exception.getMessage());
    }

    @ExceptionHandler({StockNotFoundException.class, ReorderRequestNotFoundException.class, ReorderRuleNotFoundException.class})
    public ResponseEntity<ProblemDetail> handleNotFound(RuntimeException exception) {
        return problem(HttpStatus.NOT_FOUND, exception.getMessage());
    }

    @ExceptionHandler({InsufficientStockException.class, InvalidReorderStatusException.class})
    public ResponseEntity<ProblemDetail> handleConflict(RuntimeException exception) {
        return problem(HttpStatus.CONFLICT, exception.getMessage());
    }

    private ResponseEntity<ProblemDetail> problem(HttpStatus status, String detail) {
        return ResponseEntity.status(status).body(ProblemDetail.forStatusAndDetail(status, detail));
    }
}
