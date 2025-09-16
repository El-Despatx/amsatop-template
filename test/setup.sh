#!/bin/sh
sudo apt update
sudo apt install libfuse2t64
pipx install uv
uv sync --frozen
