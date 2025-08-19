# No Cursor Setup Instructions

```sh
uv sync
uv tool install crewai
```

## Running `jupyter lab` from a terminal

VSCode and Cursor can detect the environment created by `uv`, but if you want to run Jupyter Lab from a terminal, you need to install the Jupyter kernel spec for the `agents` project.

```sh
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=agents
```

This also lets you attach to the kernel when working with [`molten.nvim`](https://github.com/benlubas/molten.nvim)

To launch Jupyter Lab in the `uv` environment:

```sh
uv run --with jupyter jupyter lab
```

In notebooks, select the `agents` kernel in the drop down.

Source: [docs.astral.sh/uv/guides/integration/jupyter/](https://docs.astral.sh/uv/guides/integration/jupyter/)
