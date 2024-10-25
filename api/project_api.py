from http import HTTPStatus

from custom_request.custom_requster import CustomRequester


class ProjectApi(CustomRequester):
    def __init__(self, session):
        super().__init__()
        self.session = session

    #Create project
    def create_project(self, project_data, expected_status_code=HTTPStatus.OK):
        return  self.send_request("POST", "/app/rest/projects", data=project_data, expected_status=expected_status_code)
    #Check project
    def get_project(self):
        return self.send_request("GET", "/app/rest/projects")
    #Create build
    def create_build_config(self, build_data, expected_status_code=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildTypes", data=build_data, expected_status=expected_status_code)
    #Check build
    def get_build(self, build_id, expected_status_code=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/buildTypes/id:{build_id}", expected_status=expected_status_code)
    #Start build
    def start_build(self, start_build_data, expected_status_code=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildQueue", data=start_build_data, expected_status=expected_status_code)
    #Check status build
    def get_status_build(self, build_type_id, expected_status_code=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/builds/buildType:{build_type_id}", expected_status=expected_status_code)

    #Delete build configuration
    def delete_build_config(self, build_config_id, expected_status_code=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/buildTypes/{build_config_id}", expected_status=expected_status_code)
    # Delete project
    def delete_project(self, project_id, expected_status_code=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/projects/id:{project_id}", expected_status=expected_status_code)
    #
    def clean_up_project(self, created_project_id):
        self.delete_project(created_project_id)
        get_project_response = self.get_project().json()
        project_ids = [project.get('id', {}) for project in get_project_response.get('project', [])]
        assert created_project_id not in project_ids, "ID created project not found in list projects after DELETE"


