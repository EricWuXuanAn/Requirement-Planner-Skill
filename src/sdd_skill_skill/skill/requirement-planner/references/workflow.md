# Workflow

1. Acquire URL requirements using the browser-only source-acquisition rules in
   `SKILL.md`: inspect existing tabs, reuse a matching URL/source, and only open
   the supplied URL when no matching tab exists. Never use Jira API scripts or
   inspect local credentials. Pasted/uploaded sources skip browser acquisition.
2. Verify the target page before extraction. Follow the bounded browser recovery
   and login handling in `SKILL.md`; continue planning once the source is read.
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
If browser access cannot acquire a URL after the recovery in `SKILL.md`, stop planning and offer pasted content,
an export, a screenshot/PDF/document, or enabling an appropriate capability.
