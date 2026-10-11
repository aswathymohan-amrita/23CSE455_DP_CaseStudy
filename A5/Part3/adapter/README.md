# Adapter

`PatientDataService` asks an `EHRProvider` for a record. `EpicEHRAdapter` is the only class that turns the nested sample into `first_name`, `last_name`, and `phone`. `EpicFHIRApi` only returns that sample.

| Language | Folder | Command |
|---|---|---|
| Java | `java/` | `javac AdapterDemo.java` then `java AdapterDemo` |
| Python | `python/` | `python adapter_demo.py` |
| JavaScript | `javascript/` | `node adapterDemo.js` |
| C++ | `cpp/` | `g++ -std=c++17 adapter_demo.cpp -o adapter_demo` |

JavaScript and C++ exit with code 1 if the three fields are wrong. Java and Python print the record. `pattern_crosslanguage.csv` compares the four versions. The prompt is in `llm/part3_prompt.txt`.
