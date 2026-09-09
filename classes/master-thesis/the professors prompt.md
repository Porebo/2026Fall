# Research-Grounded Expert Dialogue Prompt

Use this prompt to explore a thesis idea through a dialogue informed by scholars' public research. The dialogue is a thinking and research tool, not a substitute for the scholars themselves, peer discussion, or evidence.

## Core Principle

Do not ask the AI to impersonate named professors. Ask it to construct clearly fictionalized academic discussants whose perspectives are informed by the experts' verified public research interests and publications.

The goal is to use the accumulated research of relevant experts to generate search terms, concepts, questions, critiques, and possible theoretical lenses. Every factual claim and citation must later be verified in the original scholarly source.

## Reusable Prompt

```text
I am exploring this topic:
[State the topic, observation, or draft research question.]

First, research the public faculty profiles, CVs, and peer-reviewed publications of these experts:
1. [Expert name, institution, field]
2. [Expert name, institution, field]

Before beginning the dialogue, provide a brief evidence note for each expert:
- Verified research interests relevant to my topic
- Two to four relevant publications, with links or DOI when available
- Which parts of the proposed dialogue role are supported by those sources

Then create two fictionalized academic discussants informed by that evidence. Do not claim to be the named people, invent quotations, attribute opinions to them, or imply that they endorse the dialogue. Label each response as an AI synthesis informed by public scholarship.

My purpose is to test and develop ideas, not to treat the dialogue as academic evidence. Be constructively critical and distinguish clearly among:
- My observation or experience
- An interpretation of that observation
- An analogy or heuristic
- A researchable claim or proposition
- A claim needing scholarly verification

For every dialogue response:
1. Give each fictional discussant a distinct, research-grounded perspective.
2. Identify assumptions that may be too broad or unsupported.
3. Explain where an analogy is useful and where it may fail.
4. Suggest one concrete literature-search query or one next research action.
5. Do not invent citations. Mark uncertain references as unverified.

End with:
- The strongest revised research question
- A short list of concepts to define
- One next paper or search path to examine

Begin with my topic above.
```

## How To Choose Experts

Choose experts because their published work contributes a useful lens, not because they are famous or personally familiar. For one thesis topic, select complementary perspectives such as:

- An Information Quality or data-governance scholar for stewardship, quality dimensions, controls, and accountability.
- An organizational-theory or information-systems scholar for institutionalization, leadership change, incentives, routines, or technology adoption.
- A domain specialist, such as an energy-data or engineering scholar, only when the industry context needs specific interpretation.

Two experts are usually enough. Add a third only when a necessary perspective is missing.

## Use During A Dialogue

Bring concrete material. A useful turn has this shape:

```text
Observation: In my organization, data-quality work begins only after a reported ticket.

Interpretation I am considering: The removal of formal stewardship shifted the organization from preventive governance to reactive remediation.

Question: What alternative explanations should I test before treating this as deinstitutionalization of an IQ capability?
```

Ask the dialogue to challenge the interpretation, name possible rival explanations, and point you to literature. Keep a separate note of claims that require source verification.

## Guardrails

- Treat the dialogue as idea generation and rehearsal, not evidence or expert advice.
- Do not include confidential employer information, names, internal systems, or nonpublic documents.
- Use neutral language about organizations and people; describe observable practices before inferring motives.
- Read the cited papers yourself and confirm every publication, DOI, finding, and quotation.
- Consult your actual advisor, instructors, and peers for academic direction and feedback.

## Example For This Thesis Direction

```text
I am exploring: How does the dismantling of a formal Information Quality capability reshape an organization's data-quality work from preventive governance to reactive remediation?

Use a fictionalized Information Quality scholar and a fictionalized organizational-theory scholar. Ground their roles in verified public publications relevant to data governance, stewardship, deinstitutionalization, executive sponsorship, and organizational change.

Help me distinguish my firsthand observation of ticket-driven remediation from the broader claim that formal IQ capability was dismantled. Identify what evidence would support or weaken that claim, then give me precise search queries for the literature review.
```