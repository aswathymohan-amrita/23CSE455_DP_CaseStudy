package org.openwms.casestudy.ch02.exception;

public class BarcodeNotFoundException extends RuntimeException {

    public BarcodeNotFoundException(String barcode) {
        super("No stock item found for barcode: " + barcode);
    }
}
