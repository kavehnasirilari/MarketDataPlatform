# ROLE-BASED DEVELOPMENT BLUEPRINT

---

## 0. Purpose of This Blueprint
This document defines strict roles, responsibilities, and boundaries for designing and building any service or system.

Its purpose is to:

Prevent role confusion

Eliminate premature implementation

Enforce architectural discipline

Enable continuity even if individuals change

This blueprint is binding for all projects.

---

## 1. Defined Roles (Immutable)
There are **exactly three roles** in this system.

No role may assume the responsibilities of another role.
-  Architect
-  Tech Lead
-  Developer

---

## 2.Role 1 — Architect
### 2.1 Core Responsibility

The Architect is responsible for **deciding what the system is**.

Not how it is built.
Not how it is coded.

Only:

- What exists
- What does not exist
- Why those decisions were made

### 2.2 Architect Deliverables (Mandatory)
The Architect produces **one and only one primary artifact**:

```
/docs/ARCHITECTURE.md
```
This document must fully define:
- System context
- Problem definition
- Goals and non-goals
- High-level architecture
- Data flow
- Public contracts
- Failure philosophy
- Trust & security boundaries
- Evolution intent
- Open questions

If this document is missing or incomplete:

The project is not allowed to proceed.

### 2.3 Architect Explicit Restrictions (Hard Rules)
The Architect **must not**:

- Design folder structures
- Name files or modules
- Define functions or methods
- Choose implementation patterns
- Write any production code

If the Architect does any of the above:

The architectural role is violated.

### 2.4 Architect Success Criteria
The Architect has succeeded **only if**:

- The system can be defended without code
- Another person can challenge decisions meaningfully
- The document survives the Architect’s removal

## 3. Role 2 — Tech Lead
### 3.1 Core Responsibility
The Tech Lead is responsible for **translating architecture into implementable structure**.

The Tech Lead does not invent requirements.
The Tech Lead does not change intent.

The Tech Lead translates.

### 3.2 Tech Lead Input Dependency
The Tech Lead **must not start** until:
```
/docs/ARCHITECTURE.md
```
is finalized and accepted.

### 3.3 Tech Lead Deliverables (Mandatory)
The Tech Lead produces:
```
/docs/TECHNICAL_SPEC.md
```
### 3.4 Tech Lead Explicit Restrictions
The Tech Lead **must not**:

- Implement business logic
- Decide runtime behavior ad-hoc
- Modify architectural intent
- Bypass declared boundaries

The Tech Lead may suggest architectural changes **only via formal review**, not silently.

### 3.5 Tech Lead Success Criteria
The Tech Lead has succeeded if:

- Developers do not need to make architectural decisions
- All dependencies are directional and justified
- Implementation choices are constrained, not improvised

## 4. Role 3 — Developer
### 4.1 Core Responsibility
The Developer is responsible for **executing instructions exactly**.

The Developer does not reinterpret architecture.
The Developer does not invent abstractions.
The Developer does not “improve” design.

### 4.2 Developer Input Dependencies
The Developer **works only from**:

- TECHNICAL_SPEC.md
- Assigned tasks derived from it

### 4.3 Developer Deliverables
- Source code
- Tests
- Documentation limited to usage or behavior

### 4.4 Developer Explicit Restrictions
The Developer **must not**:

- Alter system boundaries
- Introduce new architectural concepts
- Redesign flows
- Make silent structural changes

If ambiguity is encountered:
&nbsp;&nbsp;&nbsp;&nbsp;The Developer must stop and escalate.

### 4.5 Developer Success Criteria
The Developer has succeeded if:

- Code matches the specification
- No architectural assumptions were made
- Changes are traceable to explicit instructions

## 5. Project Lifecycle Enforcement
Every project **must** explicitly track its stage.
```
/docs/PROJECT_STATUS.md
```
Example:
```md
Current Stage: TECH_LEAD

Architectural Design: COMPLETE
Technical Specification: IN PROGRESS
Implementation: NOT STARTED
```
Working outside the active stage is **not allowed**.

## 6. Role Switching Protocol (Critical)
When the same person plays multiple roles:

- Only one role may be active at a time
- Role switching must be explicit and intentional
- Artifacts must be completed before switching

If role boundaries blur:
&nbsp;&nbsp;&nbsp;&nbsp;Stop. Revert. Clarify.

## 7. Violation Detection Rules
If any of the following occur, the process is broken:

- Writing code before TECHNICAL_SPEC exists
- Creating folders without documented responsibility
- Defining functions without declared ownership

“Just doing it” because it feels obvious

These are **process failures**, not productivity.

## 8. Guiding Principle (Non-Negotiable)
Architecture defines possibility space.
Technical design constrains it.
Code merely occupies it.

## 9. Final Rule
If at any point you ask:
“Why does this folder / file / function exist?”

And the answer is not found in an artifact:
The system has already failed.