#!/bin/bash

echo "Making sure you have the latest version of uv.."
uv self update

echo "Running uv sync to install dependencies.."
uv sync

echo "Installing crewai uv tool.."
uv tool install crewai

echo "Installing Jupyter kernel spec for $(pwd)/.venv.."
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=agents

echo "To launch Jupyter Lab in the uv environment:"
echo " uv run --with jupyter jupyter lab"

echo "Select the 'agents' kernel in notebooks, or when running :MoltenInit"
