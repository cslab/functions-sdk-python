doc:
	uv run python -m tools.mdtable

schemas:
	uv run python -m csfunctions.tools.write_schema
