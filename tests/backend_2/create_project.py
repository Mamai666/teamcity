
import requests
import pytest

BASE_URL = "http://admin:admin@localhost:8111"


class TestProjectCreate:

    def test_project_create(self):
        auth_response = requests.get(url=f'{BASE_URL}/authenticationTest.html?csrf', auth=("admin", "admin"))
        csrf_token = auth_response.text
        headers = {"X-TC-CSRF-Token": csrf_token}
        print("CSRF Token:", csrf_token)


        #Prepare data
        project_id = "simpleprojectID2"
        project_data = {
            "parentProject": {
                "locator": "_Root"
            },
            "name": "ProjectNameSimple2",
            "id": project_id,
            "copyAllAssociatedSettings": True
        }
        print("Project Data:", project_data)

        # Create project
        create_response = requests.post(url=f'{BASE_URL}/app/rest/projects', headers=headers, json=project_data)
        assert create_response.status_code == 200, "Не удалось создать проект"


        check_project = requests.get(url=f'{BASE_URL}/app/rest/projects/id:{project_id}', headers=headers)
        assert check_project.status_code == 200, "Проект создан"


        #Prepare data for build
        build_data = {
            "id": "BuildConfID1",
            "name": "BuildConfName1",
            "project": {
                "id": project_id
            },
            "templates": {
                "buildType": [
                    {
                        "id": "MyTemplateID1"
                    }
                ]
            },
            "parameters": {
                "property": [
                    {
                        "name": "myBuildParameter1",
                        "value": "myValue1"
                    }
                ]
            },
            "steps": {
                "step": [
                    {
                        "name": "myCommandLineStep",
                        "type": "simpleRunner",
                        "properties": {
                            "property": [
                                {
                                    "name": "script.content",
                                    "value": "echo 'Hello World!'"
                                }
                            ]
                        }
                    }
                ]
            }
        }
        print("Build Data:", build_data)

        #Create build config
        create_build_config = requests.post(url=f'{BASE_URL}/app/rest/buildTypes', headers=headers, json=build_data)
        assert create_build_config.status_code == 500, "Не удалось создать конфигурацию сборки"

        #Check Build
        check_build = requests.get(url=f'{BASE_URL}/app/rest/buildTypes/BuildConfID1', headers=headers)
        assert check_build.status_code == 200, "Не удалось найти конфигурацию сборки"


        # Data for start build
        data_start_build = {
                "buildType": {
                "id": "BuildConfID1"
            }
        }

        #Start Build
        start_build = requests.post(url=f'{BASE_URL}/app/rest/buildQueue', headers=headers, json=data_start_build)
        assert start_build.status_code == 200

        #Get status build
        get_status_build = requests.get(url=f'{BASE_URL}/app/rest/buildQueue?locator=buildType(id:MyBuildConfigurationID)', headers=headers)
        assert get_status_build.status_code == 200


        # #Delete project
        # delete_project = requests.delete(url=f'{BASE_URL}/app/rest/projects/id:{project_id}', headers=headers)
        # assert delete_project.status_code == 204, "Не удалось удалить проект"
