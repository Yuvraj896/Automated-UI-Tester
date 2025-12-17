from playwright.sync_api import Page, sync_playwright, expect

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

        # put csv data
        self.csv_editor = page.get_by_role("textbox",name="Editor content;Press Alt+F1")
        
        # zoom and refresh data
        self.refresh_button = page.get_by_test_id("data-testid RefreshPicker run button")
        self.zoom_button = page.get_by_test_id("time-series-zoom-to-data")

        # Panel output (for screenshot)
        self.panel_content = page.get_by_test_id("data-testid panel content")
        self.canvas = page.get_by_test_id("uplot-main-div").locator("canvas")


        # If no data source found
        self.no_data_source = page.get_by_text("No data sources found")

        #this opens a new tab , so we need to capture it
        self.configure_data_source_link = (page.get_by_test_id("data-testid Data source list dropdown").get_by_role("link", name="Configure a new data source")
)

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

    
    def csv_file_data(self, file_path: str):
        with open(file_path, "r") as f:
            csv_data = f.read()

        # Focus editor and replace content
        self.csv_editor.click()
        self.csv_editor.fill(csv_data)

    def refresh_and_zoom(self):
        self.refresh_button.click()
        self.zoom_button.click()


    # If datasource not present
    def ensure_testdata_datasource_exists(self)-> bool :
        # If TestData already exists, nothing to do
        if self.testdata_source.is_visible(timeout=3000):
            return

        # No data sources found
        if self.no_data_source.is_visible(timeout=3000):

            # Capture the popup window
            with self.page.expect_popup() as popup_info:
                self.configure_data_source_link.click()

            datasource_page = popup_info.value

            # Search Box
            datasource_page.get_by_role("textbox", name="Filter by name or type").fill("TestData")

            # Add TestData datasource
            datasource_page.get_by_role("button", name="Add new data source TestData").click()

            # Rename datasource explicitly (good practice)
            name_input = datasource_page.get_by_test_id("data-testid Data source settings page name input field")
            name_input.click()
            name_input.press("ControlOrMeta+a")
            name_input.fill("TestData")

            # Save & Test
            datasource_page.get_by_test_id("data-testid Data source settings page Save and Test button").click()

            # Verify success
            # expect(datasource_page.get_by_test_id("data-testid Alert success")).to_contain_text("Data source is working")

            # Go back to dashboard / panel editor
            datasource_page.get_by_role("link", name="Build a dashboard").click()

            return True
        return False
