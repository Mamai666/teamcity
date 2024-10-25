from utils.datagenerator import DataGenerator


class ProjectData:
    @staticmethod
    def create_project_data():
        return {
          "parentProject": {"locator": "_Root"},
          "name": DataGenerator.fake_name(),
          "id": DataGenerator.fake_project_id(),
          "copyAllAssociatedSettings": True
        }


class BuildData:
    @staticmethod
    def create_build_data(project_id):
        return {
            "id": DataGenerator.fake_project_id(),
            "name": DataGenerator.fake_name(),
            "project": {
                "id": project_id
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
                                },
                                {
                                    "name": "teamcity.step.mode",
                                    "value": "default"
                                },
                                {
                                    "name": "use.custom.script",
                                    "value": "true"
                                }
                            ]
                        }
                    }
                ]
            }
        }

class StartBuildData:
    @staticmethod
    def start_build(build_id):
        return {
            "buildType": {
                "id": build_id
            }
        }
