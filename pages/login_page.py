# Login Page class :- Stores information about grafana login information

class LoginPage:
    def __init__(self, page):
        self.page = page

        # Locators in Login Page
        self.username_input = "input[name='user']"
        self.password_input = "input[name='password']"
        self.login_button = "button:has-text('Log in')"

        #locators in change password page
        self.new_password_input = "input[name='newPassword']"
        self.confirm_password_input = "input[name='confirmPassword']"
        self.submit_password_button = "button:has-text('Submit')"
        self.skip_button = "button:has-text('Skip')"


    def navigate(self, base_url: str):
        self.page.goto(base_url)

    def login(self, username: str, password: str, new_password: str | None = None):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

        #redirect to newPassword page
        self.change_password(new_password)

    def change_password(self, new_password : str| None):
        try:
            if self.page.locator(self.new_password_input).is_visible(timeout=3000):
                
                #if no new password is given, we will skip
                if new_password:
                    self.page.fill(self.new_password_input, new_password)
                    self.page.fill(self.confirm_password_input, new_password)
                    self.page.click(self.submit_password_button)
                else:
                    # Skip password change
                    self.page.click(self.skip_button)
        except Exception:
            # Password change screen did not appear
            pass