# pages/login_page.py

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class LoginPage:
    def __init__(self, page):
        self.page = page

        # Login Locators
        self.username_input = page.get_by_test_id("data-testid Username input field")
        self.password_input = page.get_by_test_id("data-testid Password input field")
        self.login_button = page.get_by_test_id("data-testid Login button")

        # Password change Locators
        self.new_password_input = page.get_by_role("textbox", name="New password", exact=True)
        self.confirm_password_input = page.get_by_role("textbox", name="Confirm new password")
        self.skip_password_button = page.get_by_test_id("data-testid Skip change password button")

        # Just for checking if we are at Homepage now
        self.navigation = page.get_by_role("navigation", name="Breadcrumbs")

    def navigate(self, base_url: str):
        self.page.goto(base_url)

    def login(self, username: str, password: str, new_password: str | None = None):
        # login form
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

        # Handle optional password change
        self._handle_password_change(new_password)

        # Ensure we have landed inside Grafana
        self.navigation.wait_for(timeout=10_000)

    def _handle_password_change(self, new_password: str | None):
        try:
            # If this appears, password page is active
            self.new_password_input.wait_for(timeout=5_000)

            #if no new_password is given, just skip
            if new_password:
                self.new_password_input.fill(new_password)
                self.confirm_password_input.fill(new_password)
                
            else:
                self.skip_password_button.click()

        except PlaywrightTimeoutError:
            pass
