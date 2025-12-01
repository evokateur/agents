# Week 4 – LangGraph

## Notes

### Defining the Graph

Before you call `graph.invoke(state)`

1. Define the State class

2. Start the Graph Builder

3. Create a Node

4. Create Edges
    - Repeat steps 3 and 4 until the graph is complete.

5. Compile the Graph

### The Super-Step

- >A super-step can be considered a single iteration
  >over the graph nodes. Nodes that run in parallel are
  >part of the same super-stop, while nodes that run
  >sequentially belong to separate super-steps.

- A graph describes one super-step; one interaction between agents and tools to achieve an outcome

- Every user interaction is a fresh `graph.invoke(state)` call

- *The reducer handles updating state during a super-stop but not between super-steps*

#### How it all fits together

```
[define graph] --> [super-step] --> [super-step] --> [super-step]
```

`-->`: invocation of the graph

Checkpointing occurs between super-steps to preserve state/memory

## Progress

- [x] Day 2: `1_lab1.ipynb`
  - added image_piewer.py for opening images in the default image viewer

- [x] Day 3: `2_lab2.ipynb`

- [x] Day 4: `3_lab3.ipynb`
  - NOTE: needed to run `uv run playwright install` to get the version of Chromium that matches the (uv created) `.venv`

- [x] Day 4: `4_lab4.ipynb`
  - replaced `image_viewer.py` with `monkey_see.py` (import `display` from it to override original func with version that opens temp image file in OS)

- [ ] Day 5: sidekick app
  - [ ] add memory (use example from `4_lab4.ipnynb`)
