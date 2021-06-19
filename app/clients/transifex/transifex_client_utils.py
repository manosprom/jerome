def create_resource_body(category: str, project_id: str):
    request_body = {
        "data": {
            "attributes": {
                "categories": [
                    category
                ],
                "name": category,
                "slug": category
            },
            "relationships": {
                "i18n_format": {
                    "data": {
                        "id": "KEYVALUEJSON",
                        "type": "i18n_formats"
                    }
                },
                "project": {
                    "data": {
                        "id": project_id,
                        "type": "projects"
                    }
                }
            },
            "type": "resources"
        }
    }
    return request_body
