# Week 3 – CrewAI Progress

- [x] day 1 lectures

- [x] day 2 lectures

- [x] day 3 lectures

- [x] day 4 lectures

- [x] day 5 lectures

## Project: Add to `engineering_team`

- Easy way to add to it: have team grow.
  - Test Engineer responsible for writing and executing a test plan?
  - Business Analyst responsible for gathering requirements?
- Harder way to add to it: have team build whole system, piece by piece.
  - Creating multiple modules and classes and assembling them together.
  - Requires workflow that's more interactive and iterative, no fixed number of tasks.
  - Add structured outputs
  - Add dynamic creation of tasks so that an entire set of modules can be created
    - CrewAI allows you to create a Task object at runtime.
    - [Callbacks](https://docs.crewai.com/en/concepts/tasks#callback-mechanism) can be assigned to Tasks, to be executed after task completion
