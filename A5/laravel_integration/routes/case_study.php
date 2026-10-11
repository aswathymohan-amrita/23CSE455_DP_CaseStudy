<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\CaseStudy\IntegrationController;

// Deliberately not public: all integration operations require an authenticated
// user with a privileged role. Add application-specific policies before production.
Route::middleware(['auth','verified','role:admin'])->prefix('case-study')->name('case-study.')->group(function(){
 Route::post('/lab-orders',[IntegrationController::class,'lab'])->name('lab');
 Route::post('/charges',[IntegrationController::class,'bill'])->name('billing');
 Route::get('/patients/{patientId}',[IntegrationController::class,'patient'])->name('patient');
});
