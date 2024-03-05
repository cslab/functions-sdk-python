from json import dumps

from csfunctions import DataResponse, ErrorResponse, Request, WorkloadResponse


def write_schema(output_dir="json_schemas"):
    with open(f"{output_dir}/workload_response.json", "w", encoding="utf-8") as file:
        file.write(dumps(WorkloadResponse.model_json_schema(), indent=2) + "\n")

    with open(f"{output_dir}/data_response.json", "w", encoding="utf-8") as file:
        file.write(dumps(DataResponse.model_json_schema(), indent=2) + "\n")

    with open(f"{output_dir}/error_response.json", "w", encoding="utf-8") as file:
        file.write(dumps(ErrorResponse.model_json_schema(), indent=2) + "\n")

    with open(f"{output_dir}/request.json", "w", encoding="utf-8") as file:
        file.write(dumps(Request.model_json_schema(), indent=2) + "\n")


if __name__ == "__main__":
    write_schema()
