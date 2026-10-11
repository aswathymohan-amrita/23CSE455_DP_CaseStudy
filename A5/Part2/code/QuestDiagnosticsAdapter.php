<?php
interface QuestClient { public function createOrder(array $payload): array; }
final class FakeQuestClient implements QuestClient {
 public function createOrder(array $payload): array { return ['order_id'=>'Q-'.$payload['booking_id'],'status'=>'accepted']; }
}
final class QuestDiagnosticsAdapter implements LaboratoryIntegrationInterface {
 public function __construct(private QuestClient $client) {}
 public function submitBooking(array $booking): array {
  if(!isset($booking['booking_id'],$booking['patient_id'],$booking['test_code'])) throw new InvalidArgumentException('Missing booking fields');
  $r=$this->client->createOrder(['booking_id'=>$booking['booking_id'],'patient'=>['id'=>$booking['patient_id']],'test'=>['code'=>$booking['test_code']]]);
  return ['external_reference'=>$r['order_id'],'status'=>$r['status']];
 }
}
