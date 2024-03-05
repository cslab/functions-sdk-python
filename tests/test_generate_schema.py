import filecmp
import os
import shutil
from unittest import TestCase

from csfunctions.tools.write_schema import write_schema


class TestGenerateSchema(TestCase):
    path = os.path.join(os.path.dirname(__file__), "..")
    schema_dir = os.path.join(path, "json_schemas")
    output_dir = os.path.join(path, "schema_output")

    def setUp(self) -> None:
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.output_dir)

    def test_generate_json_schema(self):
        """
        Check that the json schema matches the pydantic models, by running the schema generation and
        then comparing the new output with the existing output
        """
        write_schema(self.output_dir)
        comparison = filecmp.dircmp(self.schema_dir, self.output_dir)
        if comparison.diff_files:
            self.fail(
                f"Schema files do not match the models. Please regenerate the schema files with make schemas."
                f" {str(comparison.diff_files)}"
            )
