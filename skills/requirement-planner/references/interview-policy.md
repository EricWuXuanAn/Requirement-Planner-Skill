# Interview Policy

Ask only questions that can change at least one of:

- runtime behavior;
- implementation boundary;
- acceptance criteria;
- data, API, UI, infrastructure, migration, or compatibility scope;
- conflict resolution between source facts and project facts.

Do not ask questions answered by repository evidence. Do not ask template-filling
questions.

Each question must include:

- question ID `Q-###`;
- severity: Blocking, Important, or Non-blocking;
- why the answer matters and the impact of the answer;
- relevant source and repository evidence when available, marking missing or
  unavailable evidence explicitly;
- a recommendation when evidence supports one.

Offer two or three mutually exclusive options when the decision has natural
choices. Use an open question when forcing options would distort the issue; do
not invent choices or evidence just to satisfy a format.

Identify and ask the questions needed to clarify material requirements, requested
behavior, constraints, and implementation choices. There is no fixed question
limit. Continue with follow-up questions when answers reveal new material
uncertainties. Avoid unnecessary questions and do not ask about details already
established by evidence. Blocking questions must be resolved before the spec can
be Ready for Implementation.
