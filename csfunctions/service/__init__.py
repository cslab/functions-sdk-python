from csfunctions.service.numgen import NumberGeneratorService


class Service:
    """
    Provides access to services on the elements instance, e.g. generating numbers.
    """

    def __init__(self, service_url: str | None, service_token: str | None):
        self.generator = NumberGeneratorService(service_url, service_token)
