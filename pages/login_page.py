# Login Page class :- Stores information about grafana login information

class LoginPage:
    def __init__(self, page):
        self.page = page

    def navigate(self, base_url):
        self.page.goto(base_url)

    def login(self, username, password):
        self.page.fill("input[name='user']", username)
        self.page.fill("input[name='password']", password)
        self.page.click("button:has-text('Log in')")