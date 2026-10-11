package org.openwms.casestudy.ch02.controller;

import org.openwms.casestudy.ch02.exception.BarcodeNotFoundException;
import org.openwms.casestudy.ch02.exception.InsufficientStockException;
import org.openwms.casestudy.ch02.exception.InvalidPickingQuantityException;
import org.openwms.casestudy.ch02.exception.StockUnavailableException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class PickingExceptionHandler {

    @ExceptionHandler(BarcodeNotFoundException.class)
    public ResponseEntity<ProblemDetail> handleBarcodeNotFound(BarcodeNotFoundException exception) {
        return problem(HttpStatus.NOT_FOUND, exception.getMessage());
    }

    @ExceptionHandler(InvalidPickingQuantityException.class)
    public ResponseEntity<ProblemDetail> handleInvalidQuantity(InvalidPickingQuantityException exception) {
        return problem(HttpStatus.BAD_REQUEST, exception.getMessage());
    }

    @ExceptionHandler({InsufficientStockException.class, StockUnavailableException.class})
    public ResponseEntity<ProblemDetail> handleUnavailableStock(RuntimeException exception) {
        return problem(HttpStatus.CONFLICT, exception.getMessage());
    }

    private ResponseEntity<ProblemDetail> problem(HttpStatus status, String detail) {
        return ResponseEntity.status(status).body(ProblemDetail.forStatusAndDetail(status, detail));
    }
}
