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

        # if no source
        self.no_source_message = page.get_by_text("No data sources found")
        self.add_data_link = page.get_by_test_id("data-testid Data source list dropdown").get_by_role("link", name="Configure a new data source")

        #to search testdata
        self.filter_search = page.get_by_role("textbox", name="Filter by name or type")
        self.add_source = page.get_by_role("button", name="Add new data source TestData")

        self.data_source_naming = page.get_by_test_id("data-testid Data source settings page name input field")
        self.save_data_source_button = page.get_by_test_id("data-testid Data source settings page Save and Test button")

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


    def build_popup_page(self, popup):
        self.newPage = popup
        self.filter_search = popup.get_by_role("textbox", name="Filter by name or type")
        self.add_source = popup.get_by_role("button", name="Add new data source TestData")
        self.data_source_naming = popup.get_by_test_id("data-testid Data source settings page name input field")
        self.save_data_source_button = popup.get_by_test_id("data-testid Data source settings page Save and Test button")
        self.dashboard_load = popup.get_by_role("link", name="Build a dashboard")


    def ensure_testdata_exists(self):

        #load 
        self.panel_editor.wait_for(timeout=5000)
        
        #if the testData is already available then no need
        if self.testdata_source.is_visible(timeout=2000):
            return None
        
        #if message persists
        if self.no_source_message.is_visible(timeout=2000):
            with self.page.expect_popup() as popup_info:
                self.add_data_link.click()
            
            newPage = popup_info.value
            self.build_popup_page(newPage)

            self.filter_search.fill("TestData")
            self.add_source.click()

            self.data_source_naming.click()
            self.data_source_naming.press("ControlOrMeta+a")
            self.data_source_naming.fill("TestData")

            self.save_data_source_button.click()
            self.dashboard_load.click()

            return newPage
        
        raise RuntimeError("Unexpected datasource state")
