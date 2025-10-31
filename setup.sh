#!/bin/bash

echo "Making sure you have the latest version of uv.."
uv self update

echo "Running uv sync to install dependencies.."
uv sync

echo "Installing crewai uv tool.."
uv tool install crewai

echo "Installing Jupyter kernel spec for $(pwd)/.venv.."
uv run ipython kernel install --user --env VIRTUAL_ENV "$(pwd)/.venv" --name=agents --display-name "Agentic Engineering"
echo "Use the 'agents' kernel in Jupyter notebooks."
echo
echo "To launch Jupyter Lab in the uv environment:"
echo " uv run --with jupyter jupyter lab"
echo
echo "To launch nvim in the uv environment (for molten.nvim):"
echo " uv run nvim"
