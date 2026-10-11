<?php
declare(strict_types=1);
namespace App\Services\CaseStudy;
use Illuminate\Http\Client\Factory as HttpFactory;
use Illuminate\Support\Facades\Log;
use InvalidArgumentException;

interface LabGateway { public function submit(array $booking): array; }
final class HttpLabAdapter implements LabGateway {
    public function __construct(private HttpFactory $http, private string $url, private string $token) {}
    public function submit(array $booking): array {
        foreach (['booking_id','patient_id','test_code'] as $key) if (empty($booking[$key])) throw new InvalidArgumentException("Missing $key");
        $response=$this->http->withToken($this->token)->timeout(8)->retry(2,250)
            ->post(rtrim($this->url,'/').'/orders',[
                'clientReference'=>$booking['booking_id'],
                'subject'=>['identifier'=>$booking['patient_id']],
                'assay'=>['code'=>$booking['test_code']]
            ])->throw()->json();
        if (!is_array($response) || empty($response['orderId'])) throw new \RuntimeException('Lab response missing orderId');
        return ['external_reference'=>$response['orderId'],'status'=>$response['status']??'submitted'];
    }
}
interface BillingGateway { public function charge(int $amountMinor, string $reference): array; }
final class HttpBillingStrategy implements BillingGateway {
    public function __construct(private HttpFactory $http, private string $url, private string $token, private string $provider) {}
    public function charge(int $amountMinor, string $reference): array {
        if ($amountMinor<=0 || $reference==='') throw new InvalidArgumentException('Invalid payment');
        $response=$this->http->withToken($this->token)->withHeaders(['Idempotency-Key'=>$reference])
            ->timeout(8)->post(rtrim($this->url,'/').'/charges',[
                'amount_minor'=>$amountMinor,'reference'=>$reference
            ])->throw()->json();
        if (!is_array($response) || empty($response['transaction_id'])) throw new \RuntimeException('Billing response missing transaction');
        return ['provider'=>$this->provider,'transaction_id'=>$response['transaction_id'],'status'=>$response['status']??'pending'];
    }
}
interface PatientGateway { public function fetch(string $patientId): array; }
final class FhirPatientAdapter implements PatientGateway {
    public function __construct(private HttpFactory $http, private string $url, private string $token) {}
    public function fetch(string $patientId): array {
        if ($patientId==='') throw new InvalidArgumentException('Missing patient ID');
        $data=$this->http->withToken($this->token)->timeout(8)
            ->get(rtrim($this->url,'/').'/Patient/'.rawurlencode($patientId))->throw()->json();
        if (!is_array($data) || ($data['resourceType']??null)!=='Patient') throw new \RuntimeException('Unexpected FHIR response');
        return ['patient_id'=>$data['id']??$patientId,
            'first_name'=>$data['name'][0]['given'][0]??'',
            'last_name'=>$data['name'][0]['family']??''];
    }
}
