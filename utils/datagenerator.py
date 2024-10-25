import string
from faker import Faker

faker_instance = Faker()

class DataGenerator:
    """
    Faker для генерации данных
    """
    @staticmethod
    def fake_project_id():
        first_latter = faker_instance.random.choice(string.ascii_letters)
        rest_characters = ''.join(faker_instance.random.choices(string.ascii_letters + string.digits, k=10))
        project_id = first_latter + rest_characters
        return project_id

    @staticmethod
    def fake_name():
        return faker_instance.word()

