# Blog draft 1 — Building a small, reviewable AI project

> Draft scaffold for the intern to personalize. Replace every bracketed prompt with your own experience before publishing.

## Working title

From a CSV to a reliable service workflow: what I practiced in Week 1

## Opening

I started with a small engineering goal: [describe the task you personally found most useful]. The week moved from a clean Git setup to validating synthetic service-ticket data and thinking about model calls.

## What changed in my approach

- I used Pydantic at the data boundary so malformed rows became explicit validation errors.
- I kept logs focused on row numbers and field errors rather than repeating row contents.
- I separated a local mock from a live model API so the workflow can be exercised without a key.
- I practiced reviewing a small change before treating it as complete.

## One debugging story

[Describe a real bug you encountered, what evidence helped, and the fix you made.]

## What I would improve next

[Choose one: add a test, tighten a schema, measure cost, or improve a query. Explain why.]

## Safety note

The sample records are fictional. Real hospital, payment or client data should not be sent to a model provider during this exercise.

## Before publishing

- [ ] Remove the prompts and write truthful first-person reflections.
- [ ] Link to the commits you can explain.
- [ ] Confirm no keys or real records are included.
