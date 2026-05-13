fix:
	uv run ruff check --fix --select ALL --show-fixes --exit-zero src/
	uv run ruff format src/