from csfunctions.service.base import BaseService


class NumberGeneratorService(BaseService):
    """
    Service for generating numbers in the elements instance.
    """

    endpoint = "/numgen"

    def get_number(self, name: str) -> int:
        """
        Retrieve one number from the given generator.

        Hint: If you need more than one number use the get_numbers method instead,
        to retrieve multiple numbers in one request to the elements instance.

        :param name: name of the generator
        :return: generated number
        """
        numbers = self.get_numbers(name, 1)
        return numbers[0]

    def get_numbers(self, name: str, count: int) -> list[int]:
        """
        Retrieve multiple numbers from the given generator.

        If you need more than one number this function is more efficient to use than making multiple calls
        to get_number, because this method only performs one request to the elements instance.

        :param name: name of the generator
        :param count:  how many numbers should be generated
        :return: list of generated numbers
        """
        params = {"name": name, "count": count}
        data = self.request(self.endpoint, params=params)
        if not isinstance(data, dict):
            raise ValueError(f"Access service returned invalid data. Expected dict, got {type(data)}")
        if "numbers" not in data:
            raise ValueError(f"Access service returned invalid data. Expected 'numbers' key, got {data.keys()}")
        return data["numbers"]
