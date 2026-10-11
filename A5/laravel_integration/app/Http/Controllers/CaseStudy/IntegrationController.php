<?php
declare(strict_types=1);
namespace App\Http\Controllers\CaseStudy;
use App\Http\Controllers\Controller;
use App\Services\CaseStudy\{LabGateway,BillingGateway,PatientGateway};
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

final class IntegrationController extends Controller {
    public function lab(Request $request, LabGateway $gateway): JsonResponse {
        $payload=$request->validate([
            'booking_id'=>'required|string|max:100',
            'patient_id'=>'required|string|max:100',
            'test_code'=>'required|string|max:100'
        ]);
        return response()->json($gateway->submit($payload),202);
    }
    public function bill(Request $request, BillingGateway $gateway): JsonResponse {
        $payload=$request->validate([
            'amount_minor'=>'required|integer|min:1',
            'reference'=>'required|string|max:100'
        ]);
        return response()->json($gateway->charge((int)$payload['amount_minor'],$payload['reference']));
    }
    public function patient(string $patientId, PatientGateway $gateway): JsonResponse {
        return response()->json($gateway->fetch($patientId));
    }
}
