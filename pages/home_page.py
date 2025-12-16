class HomePage:
    def __init__(self, page):
        self.page = page

        # "+" Button on Homepage
        self.create_button = page.get_by_role("button", name="New")

        # Dashboard option inside Create menu
        self.dashboard_option = page.get_by_role("link", name="New dashboard")

    def create_dashboard(self):
        self.create_button.click()
        self.dashboard_option.click()

