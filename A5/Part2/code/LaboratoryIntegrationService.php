<?php

// Proposed Part 2 code. This file is not in esteham/hospital-management.

interface LaboratoryIntegrationInterface
{
    public function submitBooking(array $booking): array;
}

class LaboratoryIntegrationService
{
    public function __construct(private LaboratoryIntegrationInterface $laboratory)
    {
    }

    public function book(array $booking): array
    {
        return $this->laboratory->submitBooking($booking);
    }
}
