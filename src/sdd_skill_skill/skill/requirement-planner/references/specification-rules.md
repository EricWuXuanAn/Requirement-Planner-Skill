# Specification Rules

Use these ID prefixes:

| Type | Prefix |
| --- | --- |
| Source | `SRC` |
| Code Evidence | `CODE` |
| User Decision | `DEC` |
| Functional Requirement | `FR` |
| Non-functional Requirement | `NFR` |
| Acceptance Criteria | `AC` |
| Implementation Task | `IMP` |
| Test Requirement | `TR` |
| Risk | `RISK` |
| Open Question | `Q` |

Traceability chain:

```text
SRC/DEC -> FR/NFR -> CODE -> AC -> IMP -> TR
```

`IMPLEMENTATION_SPEC.md` must include:

1. Document status.
2. Requirement summary.
3. Background and problem.
4. Goals and non-goals.
5. Analysis sources and limitations.
6. Existing project implementation.
7. Confirmed decisions.
8. Functional and non-functional requirements.
9. User or system flows.
10. Applicable UI, API, data, infrastructure, or domain sections.
11. Modification and non-modification scope.
12. Confirmed and probable modification locations.
13. Compatibility and regression impact.
14. Boundaries and error scenarios.
15. Acceptance criteria.
16. Implementation tasks and order.
17. Verification plan.
18. Risks, assumptions, and open questions.
19. Evidence index.
20. Traceability matrix.

Mark inapplicable sections as not applicable. Do not force Android, Web, Backend,
or any other domain-specific structure without evidence.
