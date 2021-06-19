import json
import urllib.parse
import urllib.parse as url

import requests

from app.clients.transifex.transifex_client_utils import create_resource_body


class TransifexClient(object):

    def __init__(self, base_url: str, token: str, organization: str = None, project: str = None):
        self.base_url = base_url
        self.token = token
        self.organization = organization
        self.project = project

    def get_resource(self, resource: str):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        id = self.__create_id(self.organization, self.project, resource)
        response = requests.get(self.create_path(self.base_url, ["resources", id]), headers=headers)
        response.raise_for_status()
        return response.json()

    def get_resources(self):
        query_params = {
            'filter[project]': self.__create_id(organization=self.organization, project=self.project)
        }
        response = requests.get(self.create_path(self.base_url, ["resources"]), params=query_params)
        response.raise_for_status()
        return response.json()

    def create_resource(self, category: str):
        request_body = create_resource_body(category, self.__create_id(organization=self.organization, project=self.project))
        headers = {
            'content-type': 'application/vnd.api+json',
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.post(self.create_path(self.base_url, ["resources"]), json=request_body, headers=headers)
        response.raise_for_status()
        return response.json()

    def resource_strings_upload(self, category, data):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        files = {
            'content': json.dumps(data)
        }

        data = {
            "resource": self.__create_id(organization=self.organization, project=self.project, resource=category)
        }

        response = requests.post(self.create_path(self.base_url, ["resource_strings_async_uploads"]), data=data, files=files, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def __create_id(organization: str = None, project: str = None, resource: str = None):
        id = []

        if organization:
            id.append("o:" + organization)

        if project:
            id.append("p:" + project)

        if resource:
            id.append("r:" + resource)

        return ":".join(id)

    @staticmethod
    def create_path(host: str = None, path: list[str] = None):
        return url.urljoin(host, "/".join(path))
