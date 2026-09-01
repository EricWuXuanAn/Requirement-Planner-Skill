# Compatibility

The core skill is vendor-neutral and can be read by any agent that can access
repository files. The installer provides first-version adapters for Codex,
Claude, and generic repository instructions.

Full support requires:

- file read access;
- for URL requirements, an available user-authorized browser, issue tracker
  connector, or other source-reading capability;
- ability to run the inspection and validation scripts or accept their output
  manually;
- ability to ask the user follow-up questions;
- ability to write planning documents after user confirmation.

Agents without shell access can still follow the workflow manually, but must
record any unavailable source or repository evidence rather than guessing.
