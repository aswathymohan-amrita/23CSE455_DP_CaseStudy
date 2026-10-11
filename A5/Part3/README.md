# Part 3

Two patterns, four languages. The adapter programs are Pravallika's part. The strategy programs are Manogna's part.

`adapter/` is the EHR patient record. The program asks for patient `PT-98765` and prints John, Smith, and `555-1234`.

`strategy/` is the diagnostic payment. One run charges `DX-1001` through Stripe and `DX-1002` through PayPal.

Open the language folder and follow its README. Java, Python, JavaScript  and C++ use the same roles. Nothing in these programs calls a network. The output we captured is in `data/test_result/`.
