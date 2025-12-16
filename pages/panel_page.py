# pages/panel_page.py

class PanelPage:
    def __init__(self, page):
        self.page = page

        self.testdata_source = page.get_by_role("button", name="TestData Tags TestData")

        # to check if editor have Visualization tab
        self.panel_editor = page.get_by_test_id("data-testid Panel editor content")

        self.visualization_picker= page.get_by_test_id("data-testid toggle-viz-picker")
        self.timeseries_option = page.get_by_text("Time series", exact=True)

        # Visualization with
        self.query_type_dropdown = page.locator(".css-1ms3s8l-input-suffix > .css-1d3xu67-Icon").first
        self.csv_content_option = page.get_by_text("CSV Content", exact=True)

    def select_testdata_source(self):
        self.testdata_source.click()

        # Wait until panel editor fully loads
        self.panel_editor.wait_for(timeout=10_000)

    def select_timeseries_visualization(self):
        self.visualization_picker.click()
        self.timeseries_option.wait_for(timeout=5_000)
        self.timeseries_option.click()

    def select_query_type(self):
        self.query_type_dropdown.click()

        # Drop Down and Now CSV Content exists
        self.csv_content_option.wait_for(timeout=5_000)
        self.csv_content_option.click()