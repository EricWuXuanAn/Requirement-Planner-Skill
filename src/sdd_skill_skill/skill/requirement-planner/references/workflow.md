# Workflow

1. Acquire the source requirement through a capability available to the current
   agent. For authenticated URLs, use a user-authorized browser or connector;
   never collect credentials in chat or from credential storage.
2. If authentication is required, pause, ask the user to authenticate in the
   provided interface, wait for confirmation, reload the original URL, and verify
   the target source before extracting anything.
3. Create or update the source snapshot.
4. Inspect the repository instructions, documentation, build/dependency files,
   source roots, tests, schemas, migrations, resources, and relevant code.
5. Build an evidence index with stable IDs.
6. Identify facts, conflicts, gaps, risks, and engineering inferences.
7. Interview the user for blocking and important implementation choices only.
8. Summarize decisions and wait for confirmation.
9. Generate implementation and test specifications.
10. Run the installed standalone `scripts/validate_spec.py` against the
    implementation specification.
11. If validation has errors, fix the specification and repeat validation until
    there are no errors. Do not complete handoff while errors remain.
12. Stop and wait for implementation instructions.

Do not skip repository inspection even when the requirement source appears clear.
Do not mark a document Ready when blocking questions remain.
If no source capability can access a URL, stop planning and offer pasted content,
an export, a screenshot/PDF/document, or enabling an appropriate capability.
