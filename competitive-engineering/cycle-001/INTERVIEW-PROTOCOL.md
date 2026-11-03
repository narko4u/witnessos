# Contractor interview protocol: test and tag records

Purpose: establish whether independently verifiable records are a purchasing driver, before any production code is written. This is a research instrument, not a sales call.

Five operators. 20 to 30 minutes each. Their own register open on the table or screen where possible.

## Rules for the interviewer

1. Ask the question as written, then stop talking. Silence gets the second sentence and the second sentence is usually the truth.
2. Never introduce the product. If asked what we are building, say: "software for keeping the register, still in research" and return to their answers.
3. Record negative evidence with the same care as positive. "Never been challenged" is a result.
4. Do not accept an adjective where a number belongs. "Ages" is followed by "roughly how long, hours or days?".
5. Note the exact software name and the exact price they pay. Ask to see the invoice if they will.
6. Write the quotes down verbatim. Paraphrase destroys the evidence class.
7. Every question gets an evidence class in the sheet: E0 opinion, E1 their claim, E2 reproduced in front of us, E3 measured, E4 documented by a third party.

## Questions

**Q1. Have you ever had a test and tag record questioned?**
By a client, a principal contractor, an auditor, an insurer or a regulator. If yes: what year, what was questioned, who raised it. If no: has anyone ever asked to see the records at all and in what form?

**Q2. What did you have to produce to settle it?**
Paper tag, PDF report, CSV, a photo, a second visit, the tester's own memory. How long did it take, in hours or site visits and who paid for that time?

**Q3. Do you trust the CSV or PDF reports you hand over?**
Follow-up: how would you prove one of them was not altered, if someone said it was? What would you do if a client claimed a page had been changed?

**Q4. Would a record the client could verify without contacting you change anything?**
Ask last, after the history questions, so it does not contaminate them. Then: would it change what you charge, what you win or nothing at all?

**Q5. How often do your technicians work with no reliable signal?**
Which sites, how long, what happens to the record in that time today. What do they do when the app will not save?

**Q6. Which tester do you run?**
Make and model, how many and whether readings are typed, imported or ignored. Do the readings go to the client and does anyone ask for them?

**Q7. What software holds your register today?**
Name, version if known, what it costs per month or per year, what you like and the last time it annoyed you enough to mention it.

**Q8. What do you pay in total, including the parts you do not use?**
Software, tags, printer, tester, plus the labour hours spent on records per round. Rounding is fine, but make it a number.

**Q9. What would make you switch?**
Then test the answer: would X alone do it or does it need Y as well. Do not offer our features as one of the options.

**Q10. Would you pay A$59 a month solo or A$149 a month for up to five technicians?**
Ask cold, before any demonstration. Record the first reaction, not the considered one. Follow-up: what do you pay now and is the difference the reason for your answer?

**Q11. Would you run a pilot on your own tags and register?**
What would you need to see first and what would make you stop.

## Capture sheet, one per operator

| Field | Value |
|---|---|
| Operator, suburb, size (technicians) | |
| Register software and price | |
| Tester make and model | |
| Q1 challenged: never / once / repeatedly | |
| Q2 evidence produced, time cost | |
| Q3 trusts own reports: yes / no / depends | |
| Q4 verifiable record matters: not at all / nice / would pay | |
| Q5 no-signal frequency | |
| Q9 switch trigger | |
| Q10 reaction to A$59 / A$149 | |
| Q11 pilot: yes / no / conditions | |
| Verbatim quotes | |

## Decision rule, fixed before the calls

- **Two or more of five** report an actual record challenge with real time lost: the evidence claim survives as a purchasing driver and VoltLedger keeps its differentiation score.
- **One or none**: independently verifiable evidence is not a buying trigger. Re-score VoltLedger with differentiation reduced and either find a different advantage demonstrated in the interviews or demote the candidate. No rationalising around it.
- **Three or more** report losing records to connectivity or app failure: offline and durability become the lead claim instead, since that is measurable in a demo.
- Any operator who names a competitor we did not survey: add it to the register with an evidence class.
