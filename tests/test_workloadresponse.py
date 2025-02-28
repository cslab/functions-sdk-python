from unittest import TestCase

from pydantic import TypeAdapter

from csfunctions import Response, WorkloadResponse
from csfunctions.actions import AbortAndShowErrorAction


class TestWorkloadResponse(TestCase):
    def test_discriminator(self) -> None:
        """
        Test that the discriminator on action objects (and responses) works
        """

        # create some workload response with an action and serialize it
        response_json = WorkloadResponse(actions=[AbortAndShowErrorAction(message="123")]).model_dump_json()

        # parse the json with the Pydantic TypeAdapter to turn the json back into a Response object
        response_obj: WorkloadResponse = TypeAdapter(Response).validate_json(response_json)
        action_obj = response_obj.actions[0]

        # check that the objects are of the correct type again
        self.assertIsInstance(response_obj, WorkloadResponse)
        self.assertIsInstance(action_obj, AbortAndShowErrorAction)
