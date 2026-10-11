<?php
declare(strict_types=1);
namespace App\Providers;
use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Http;
use App\Services\CaseStudy\{LabGateway,HttpLabAdapter,BillingGateway,HttpBillingStrategy,PatientGateway,FhirPatientAdapter};

require_once __DIR__.'/../Services/CaseStudy/Integrations.php';

final class CaseStudyIntegrationProvider extends ServiceProvider {
    public function register(): void {
        $this->app->bind(LabGateway::class,fn($app)=>new HttpLabAdapter(
            Http::getFacadeRoot(),(string)config('case_study.lab.url'),(string)config('case_study.lab.token')));
        $this->app->bind(BillingGateway::class,fn($app)=>new HttpBillingStrategy(
            Http::getFacadeRoot(),(string)config('case_study.billing.url'),(string)config('case_study.billing.token'),
            (string)config('case_study.billing.provider','sandbox')));
        $this->app->bind(PatientGateway::class,fn($app)=>new FhirPatientAdapter(
            Http::getFacadeRoot(),(string)config('case_study.patient.url'),(string)config('case_study.patient.token')));
    }
}
