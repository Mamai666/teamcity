from custom_request.custom_requster import CustomRequester


class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.auth_and_get_csrf()

    def auth_and_get_csrf(self):
        self.session.auth = ("admin", "admin")
        csrf_token = self.send_request("GET", "/authenticationTest.html?csrf").text
        if not csrf_token:
            raise ValueError("CSRF token is missing or invalid")
        self._update_header(**{"X-TC-CSRF-Token": csrf_token})