# 23CSE455_DP_CaseStudy

# Design Pattern Identification and Evolution

## Project Overview

This project analyzes design patterns in a Next.js-based Healthcare Appointment Management System.

**Repository:** https://github.com/arnobt78/HealthCare-Doctor-Appointment-Management-System--NextJS-FullStack

The analysis classifies patterns into three categories:
- Implemented patterns
- Pattern-like structures
- Refactoring opportunities

## Project Files

| File | Description |
|---|---|
| `patterns.csv` | Final validated design-pattern records and supporting evidence |
| `pattern_counts.csv` | Counts and summary of the validated pattern records |
| `README.md` | Project overview, methodology, and findings |

## Final Pattern Classifications

| Pattern | Category | Classification |
|---|---|---|
| Singleton | Creational | Pattern-like |
| Factory | Creational | Pattern-like |
| Observer | Behavioral | Refactoring opportunity |
| Strategy | Behavioral | Refactoring opportunity |
| State | Behavioral | Refactoring opportunity |
| Command | Behavioral | Refactoring opportunity |
| Adapter | Structural | Refactoring opportunity |

## Summary

- **Implemented GoF patterns:** 0
- **Pattern-like structures:** 2
- **Refactoring opportunities:** 5
- **Total validated records:** 7

## Evidence and Rationale

### 1. Singleton-like structure
**File:** `lib/appwrite.config.ts`

The application creates a shared Appwrite client and exports service instances. It is classified as pattern-like because it does not implement a canonical Singleton class or explicit `getInstance()` method.

### 2. Factory-like structure
**File:** `lib/validation.ts`

The `getAppointmentSchema(type)` function selects a validation schema based on the appointment operation. It resembles a simple factory but does not establish the GoF Factory Method pattern.

### 3. Observer — Refactoring Opportunity
**File:** `lib/actions/appointment.actions.ts`

Appointment updates directly trigger SMS notifications. An Observer-based design could decouple appointment changes from notification delivery.

### 4. Strategy — Refactoring Opportunity
**File:** `components/forms/AppointmentForm.tsx`

Conditional logic selects appointment behavior. Separate strategies could be useful if appointment rules become more complex.

### 5. State — Refactoring Opportunity
**Files:** `types/index.d.ts`, `components/forms/AppointmentForm.tsx`

The application uses `pending`, `scheduled`, and `cancelled` appointment statuses. Explicit state objects could be considered if lifecycle behavior becomes more complex.

### 6. Command — Refactoring Opportunity
**File:** `lib/actions/appointment.actions.ts`

Appointment operations are implemented as action functions. Command objects could support queued, auditable, or retryable operations.

### 7. Adapter — Refactoring Opportunity
**Files:** `lib/appwrite.config.ts`, `lib/actions/appointment.actions.ts`, `lib/actions/patient.actions.ts`

An application-defined adapter could isolate Appwrite-specific operations if support for alternative infrastructure providers is required.

## Counting Methodology

1. Count each validated pattern record once.
2. Separate baseline findings from future evolved versions.
3. Distinguish implemented patterns, pattern-like structures, and refactoring opportunities.
4. Do not count proposed patterns as currently implemented.
5. Exclude patterns rejected during source-code validation.
6. Update classifications only when new source-code evidence supports the change.

## Limitations

These findings describe the reviewed baseline code. The five refactoring opportunities are proposed improvements, not implemented patterns. Future versions must be reviewed independently before their pattern classifications and counts are updated.

## Conclusion

The baseline analysis contains seven validated records: two pattern-like structures and five refactoring opportunities. No canonical GoF design pattern was validated as fully implemented under the project's strict classification criteria.
