import json
import urllib.parse

import pytest
import responses

from app.clients.transifex.transifex_client import TransifexClient
from tests.utils import load_test_resource


class TestTransifexClient:

    @pytest.fixture
    def transifex_client(self):
        return TransifexClient(
            base_url="https://transifex.api",
            token="some_token",
            organization="an_organization",
            project="a_project"
        )

    def test_create_id_should_include_organization(self, transifex_client):
        # Given
        organization_id = "an_organization"

        # When
        id = transifex_client._TransifexClient__create_id(organization=organization_id)

        # Then
        assert id == "o:an_organization"

    def test_create_id_should_include_project(self, transifex_client):
        # Given
        project_id = "a_project"

        # When
        id = transifex_client._TransifexClient__create_id(project=project_id)

        # Then
        assert id, "p:a_project"

    def test_create_id_should_include_resource(self, transifex_client):
        # Given
        resource_id = "a_resource"

        # When
        id = transifex_client._TransifexClient__create_id(resource=resource_id)

        # Then
        assert id == "r:a_resource"

    def test_create_id_should_combine_all_identifiers(self, transifex_client):
        # Given
        organization_id = "an_organization"
        project_id = "a_project"
        resource_id = "a_resource"

        # When
        id = transifex_client._TransifexClient__create_id(organization=organization_id, project=project_id, resource=resource_id)

        # Then
        assert id == "o:an_organization:p:a_project:r:a_resource"

    @responses.activate
    def test_get_resource_should_request_and_return_response(self, transifex_client):
        # Given
        resource = "a_resource"

        expected_resource_response = json.loads(load_test_resource("clients/transifex/mocked_get_resource_response.json"))

        responses.add(
            responses.GET,
            "https://transifex.api/resources/o:an_organization:p:a_project:r:a_resource",
            json=expected_resource_response,
            status=200
        )

        # When
        actual_resource_response = transifex_client.get_resource(resource=resource)

        # Then
        assert responses.calls[0].request.url == "https://transifex.api/resources/o:an_organization:p:a_project:r:a_resource"
        assert actual_resource_response == expected_resource_response

    @responses.activate
    def test_get_resources_should_request_and_return_response(self, transifex_client):
        # Given
        expected_resources_response = json.loads(load_test_resource("clients/transifex/mocked_get_resources_response.json"))
        expected_project_filter = {
            "filter[project]": "o:an_organization:p:a_project"
        }
        responses.add(
            responses.GET,
            url='https://transifex.api/resources?' + urllib.parse.urlencode(expected_project_filter),
            json=expected_resources_response,
            status=200
        )

        # When
        actual_resource_response = transifex_client.get_resources()

        # Then
        assert actual_resource_response == expected_resources_response

    @responses.activate
    def test_create_resource_should_create_and_return_a_resource(self, transifex_client):
        # Given
        category = "entertainment"

        expected_create_resource_request = json.loads(load_test_resource("clients/transifex/mocked_create_resource_request.json"))
        expected_create_resource_response = json.loads(load_test_resource("clients/transifex/mocked_create_resource_response.json"))

        responses.add(
            responses.POST,
            url='https://transifex.api/resources',
            json=expected_create_resource_response,
            status=200
        )

        # When
        actual_resource_response = transifex_client.create_resource(category)

        # Then
        assert json.loads(responses.calls[0].request.body) == expected_create_resource_request
        assert responses.calls[0].request.headers['content-type'] == 'application/vnd.api+json'
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer some_token'
        assert actual_resource_response == expected_create_resource_response

    @responses.activate
    def test_resource_strings_upload_should_upload_data(self, transifex_client):
        # Given
        category = "entertainment"
        expected_resource_string_upload_response = json.loads(load_test_resource("clients/transifex/mocked_resource_strings_upload_response.json"))

        given_data = {
            "test_1_key": "test_1_value",
            "test_2_key": "test_2_value"
        }

        responses.add(
            responses.POST,
            url='https://transifex.api/resource_strings_async_uploads',
            json=expected_resource_string_upload_response,
            status=200
        )

        # When
        actual_resource_response = transifex_client.resource_strings_upload(category, given_data)

        # Then
        # assert json.loads(responses.calls[0].request.body) == expected_create_resource_request
        assert responses.calls[0].request.headers['content-type'].startswith('multipart/form-data;')
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer some_token'
        assert actual_resource_response == expected_resource_string_upload_response
