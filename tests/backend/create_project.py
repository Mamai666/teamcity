import time

import requests
import pytest

from conftest import api_manager
from custom_request.custom_requster import CustomRequester
from data.project_data import ProjectData
from data.project_data import BuildData
from data.project_data import StartBuildData


class TestProjectCreate:

    @classmethod
    def setup_class(cls):
        cls.project_data = ProjectData.create_project_data()
        cls.create_project_id = cls.project_data["id"]

        cls.build_data = BuildData.create_build_data(cls.create_project_id)
        cls.create_build_id = cls.build_data["id"]

        cls.start_build_data = StartBuildData.start_build(cls.create_build_id)
        cls.start_build_id = cls.start_build_data


    def test_project_create(self, api_manager):
        # Create project
        create_project_response = api_manager.project_api.create_project(self.project_data).json()
        assert create_project_response.get("id", {}) == self.create_project_id
        #Check project
        get_project_response =  api_manager.project_api.get_project().json()
        project_ids = [project.get('id', {}) for project in get_project_response.get('project', [])]
        assert self.create_project_id in project_ids

        #Create build config
        create_build_response = api_manager.project_api.create_build_config(self.build_data).json()
        assert create_build_response.get("id", {}) == self.create_build_id
        #Check build config
        get_build_response = api_manager.project_api.get_build(self.create_build_id).json()
        assert get_build_response.get('id') == self.create_build_id

        #Start build
        start_build_response = api_manager.project_api.start_build(self.start_build_data).json()
        assert start_build_response is not None
        time.sleep(10)
        #Check status build
        get_status_build_response = api_manager.project_api.get_status_build(self.create_build_id).json()
        assert get_status_build_response.get('status') == "SUCCESS", "Сборка не завершилась успешно!"

        # #Delete build config
        api_manager.project_api.delete_build_config(self.create_build_id)

        #Delete project
        api_manager.project_api.delete_project(self.create_project_id)