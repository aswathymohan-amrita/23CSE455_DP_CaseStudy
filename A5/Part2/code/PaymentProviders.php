<?php
// Fake providers; no external transactions.
final class StripePayment implements PaymentStrategy {
 public function processPayment(float $amount,string $reference): array {
  if($amount<=0||$reference==='') throw new InvalidArgumentException('Invalid payment');
  return ['provider'=>'stripe','amount'=>$amount,'reference'=>$reference,'status'=>'paid'];
 }
}
final class PayPalPayment implements PaymentStrategy {
 public function processPayment(float $amount,string $reference): array {
  if($amount<=0||$reference==='') throw new InvalidArgumentException('Invalid payment');
  return ['provider'=>'paypal','amount'=>$amount,'reference'=>$reference,'status'=>'paid'];
 }
}
