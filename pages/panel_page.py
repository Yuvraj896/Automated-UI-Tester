#creating new dashbord using table data source

class PanelPage:
    def __init__(self, page):
        self.page = page

    def select_timeseries(self):
        # Ensure visualization tab is visible
        self.page.click("text=Visualization")
        self.page.click("text=Time series")

    def select_testdata_datasource(self):
        # Click data source selector
        self.page.click("text=Select data source")
        self.page.click("text=TestData")

    def add_static_csv(self, csv_data):
        # Select scenario (CSV content)
        self.page.click("text=Scenario")
        self.page.click("text=CSV content")

        # Fill CSV data
        self.page.fill("textarea", csv_data)

    def apply_panel(self):
        self.page.click("text=Apply")