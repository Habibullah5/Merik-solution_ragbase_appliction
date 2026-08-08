# Merik Solutions Engineering Handbook

Version 4.2 · Last updated 12 June 2026 · Owner: Engineering Operations

This handbook sets out how engineering works at Merik Solutions: what is
expected of you, how code reaches production, and what happens when something
goes wrong. It applies to every engineer, including interns and contractors.

Where this document and a customer contract disagree, the contract wins.
Where it and the employment handbook disagree on pay, leave or benefits, the
employment handbook wins.

---

## 1. Working at Merik

### 1.1 Hours and availability

Core hours are 11:00 to 16:00 Pakistan Standard Time. Outside those hours you
are trusted to work when you work best. Engineers are expected to be reachable
during core hours on the day they are on call, and not otherwise.

There is no expectation that you answer messages in the evening. If something
genuinely cannot wait until morning it goes through the on-call rota described
in section 6, not through a direct message to whoever is awake.

### 1.2 Remote and office

Merik is remote first. The Lahore office is available to anyone who wants a desk
and is booked through the internal rota. Teams may agree on one shared in-office
day per week; nobody is required to attend more than that.

### 1.3 Equipment

New engineers receive a laptop, an external display and a budget of PKR 60,000
for a chair, desk or peripherals. Claim it through Finance within your first
ninety days. After ninety days the budget lapses and cannot be reinstated.

Replacement cycles are three years for laptops and five years for displays. If a
machine fails before then, raise ticket type `IT-HW` and you will be issued a
loan machine within one working day.

---

## 2. Code and review

### 2.1 Branching

Work happens on short-lived branches cut from `main`. A branch that has been
open for more than five working days should either be merged or split. Long
branches are the most common cause of painful merges at Merik and we would
rather review three small changes than one large one.

Branch names follow `type/short-description`, where type is one of `feat`,
`fix`, `chore`, `docs` or `spike`.

### 2.2 Review expectations

Every change to a production repository requires one approving review. Changes
that touch authentication, billing or data deletion require two, and at least
one of those must come from the owning team.

Reviewers are expected to respond within one working day. If you cannot review
something in that window, say so in the thread rather than leaving it silent.
A review that arrives late is inconvenient; a review that never arrives blocks
a colleague indefinitely.

Note that the two-approval rule does not apply to enterprise customer
integrations, which follow the separate change process in section 2.6.

### 2.3 What a reviewer looks for

In rough priority order:

1. Does it do what the description says it does?
2. Is it tested where a failure would be expensive?
3. Will the next engineer understand it without asking the author?
4. Is it consistent with how the rest of the repository works?
5. Style, naming and formatting.

Points one to three are worth commenting on. Point five is worth automating and
should rarely appear in a human review.

### 2.4 Test requirements

Merge is blocked unless the automated suite passes. Coverage is measured but not
gated; a coverage number is a signal, not a target, and code written to satisfy
a percentage is usually worse than code written to be correct.

New code paths that handle money, personal data or irreversible actions require
a test. This is not negotiable and reviewers are expected to enforce it.

### 2.5 Dependencies

Adding a dependency is a long-term commitment made in thirty seconds. Before
adding one, check that it is maintained, that its licence is compatible, and
that the problem is not three lines of code you could own outright.

All dependency versions are pinned in a committed lockfile. Unpinned versions
are treated as a build defect.

### 2.6 Enterprise change process

Changes to enterprise customer integrations require a signed change request,
a nominated rollback owner, and a deployment window agreed with the customer.
This process adds roughly two working days and exists because these customers
have contractual notice periods.

---

## 3. Deployment

### 3.1 Release cadence

Teams deploy when their change is ready. There is no release train and no
freeze except the one described in section 3.5.

### 3.2 Environments

| Environment | Purpose | Who can deploy |
| --- | --- | --- |
| `local` | Development | Anyone |
| `preview` | Per-branch preview builds | Automatic on push |
| `staging` | Integration and QA | Anyone on the owning team |
| `production` | Live | Owning team, after review |

Preview environments are destroyed seven days after the branch is merged or
closed. Do not treat a preview URL as durable.

### 3.3 Rollback

Every deployment must be reversible within ten minutes. If a change cannot be
rolled back, it must be shipped behind a flag that can be turned off.

To roll back, run the deployment pipeline against the previous release tag. Do
not roll back by reverting the commit and redeploying: that is slower and it
loses the record of what actually happened.

### 3.4 Feature flags

Flags are for shipping incomplete work safely, not for permanent configuration.
A flag older than sixty days is reported to the owning team weekly until it is
removed. Flags that have been fully rolled out should be deleted along with the
dead branch of code behind them.

### 3.5 Deployment freeze

There is one annual freeze, from 24 December to 2 January inclusive. During the
freeze only fixes for severity one incidents may be deployed, and they require
approval from the on-call lead.

---

## 4. Data and privacy

### 4.1 Classification

| Class | Examples | Handling |
| --- | --- | --- |
| Public | Marketing copy, docs | No restriction |
| Internal | Architecture notes, roadmaps | Merik accounts only |
| Confidential | Customer records, contracts | Named access, logged |
| Restricted | Credentials, keys, health data | Named access, encrypted, audited |

### 4.2 Customer data in development

Production customer data must never be copied into a development or staging
environment. If you need realistic data, use the synthetic generator in
`merik-tools/fixtures`, which produces structurally identical records with no
real people in them.

The single exception is a severity one incident, where a named engineer may be
granted time-boxed read access to production by the on-call lead. That access
expires automatically after four hours and every query is logged.

### 4.3 Retention

Customer records are retained for seven years after account closure, which is
the statutory minimum for our contracts. Application logs are retained for
ninety days. Prompt and response logs from AI features are retained for thirty
days and are excluded from the seven year rule.

### 4.4 Deletion requests

A verified deletion request is completed within thirty days. Deletion covers
production records, backups on their next rotation, and any derived index or
embedding store. The last of those is the one teams forget: if a customer
record has been embedded into a vector index, deleting the row is not enough.

---

## 5. Security

### 5.1 Credentials

No secret may be committed to a repository, ever, including in a branch that
is never merged. Secrets live in the secret manager and reach the application
through environment variables at deploy time.

If a secret reaches a repository, treat it as compromised. Rotate it first,
then clean the history. Rotating takes minutes; assuming nobody noticed takes
one scraper to disprove.

### 5.2 Access

Access is granted by role, reviewed quarterly, and revoked on the last working
day. Requests for standing production write access are declined by default;
if you need it for a specific piece of work, request it time-boxed.

### 5.3 Reporting a suspected incident

Report anything suspicious to the security channel immediately, including
things you are not sure about. Merik has never disciplined anyone for a false
alarm and has no intention of starting.

### 5.4 Known error codes

These identifiers appear in logs and support tickets. They are exact strings
and will not be found by meaning alone.

| Code | Meaning | First action |
| --- | --- | --- |
| `MRK-4471` | Upstream auth token expired mid-request | Retry once; if it persists, rotate |
| `MRK-4472` | Token valid but scope insufficient | Check the role assignment |
| `MRK-5010` | Rate limit reached on the model provider | Back off with jitter, do not retry immediately |
| `MRK-5011` | Token-per-minute ceiling reached | Queue the work, reduce prompt size |
| `MRK-6203` | Vector index unavailable | Fall back to keyword retrieval, page the on-call |
| `MRK-6204` | Embedding model version mismatch | Re-embed the affected corpus |
| `MRK-7788` | Deletion job failed on a derived index | Escalate within one hour, see section 4.4 |

---

## 6. Incidents

### 6.1 Severity

**Severity one.** Customers cannot use the product, or data is at risk.
Response begins immediately, day or night.

**Severity two.** A significant feature is broken, or performance is badly
degraded. Response begins within one hour during working hours.

**Severity three.** Something is wrong but customers can still work. Handled in
the normal course of the week.

### 6.2 On call

Each team runs a weekly rota. The on-call engineer is expected to acknowledge a
severity one page within fifteen minutes and to have help if they need it: the
rota exists so that one person notices, not so that one person fixes everything
alone.

On-call weeks are compensated at the rate set out in the employment handbook,
which is a separate document and not covered here.

### 6.3 During an incident

One person runs the incident and does not also debug it. Their job is to keep
a timeline, decide what gets communicated, and pull in whoever is needed.

Communicate early and plainly. "We are investigating reports of failed logins"
is a better first message than a precise explanation twenty minutes later.

### 6.4 Afterwards

Every severity one and severity two incident gets a written review within five
working days. The review describes what happened, what the contributing causes
were, and what changes follow. It does not name individuals as causes.

Reviews are published internally. An incident nobody can read about is an
incident the company learns nothing from.

---

## 7. AI features

### 7.1 Prompts are code

Prompts live in versioned files in the repository, not inline in application
code. Every response is logged with the prompt version that produced it. This
is the only way to answer the question "what did we actually send" after the
fact.

### 7.2 Evaluation before launch

No AI feature reaches production without an evaluation suite that runs in one
command and reports a score. Twenty real cases with expected outputs is the
minimum, and cases are added every time the feature is wrong in the wild.

### 7.3 Grounding and refusal

Any feature that answers questions about Merik or customer data must answer
only from supplied passages, must cite the passage it used, and must refuse
when the passages do not contain the answer. Refusal rate is monitored: a
sudden rise almost always means retrieval has broken rather than that questions
got harder.

### 7.4 Cost

Every AI feature has a monthly cost ceiling agreed before launch and an alert
at eighty per cent of it. Cost per request is tracked as a trend, because the
usual failure is not a spike but a slow climb as prompts quietly grow.

### 7.5 What we do not do

We do not use customer data to train models. We do not deploy a feature whose
output is shown to a customer without a human-reviewed evaluation. We do not
let an agent take an irreversible action, including anything that moves money
or deletes data, without a human approving that specific action.

---

## 8. Documentation

### 8.1 The README

Every repository opens with what it does in one paragraph, then exact commands
that work from a fresh clone. If a new engineer cannot run it within five
minutes, the README is incomplete regardless of how much else it contains.

### 8.2 Decision records

Decisions that were hard, contested or expensive get a short record: what we
chose, what we rejected, and why. Two paragraphs is usually enough. The value
is not the decision, it is that the next person can tell whether the reasoning
still holds.

### 8.3 Comments

Comment why, not what. Code already says what it does. If it does not, the fix
is usually clearer code rather than a longer comment.

---

## 9. Contacts

Engineering Operations owns this handbook. Suggestions and corrections go
through the internal support form; the queue is reviewed weekly.

Questions about pay, leave, visas or benefits are not covered by this document
and belong to People Operations.
