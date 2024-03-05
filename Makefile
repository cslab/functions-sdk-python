doc:
	poetry run python -m tools.mdtable

schemas:
	poetry run python -m csfunctions.tools.write_schema
