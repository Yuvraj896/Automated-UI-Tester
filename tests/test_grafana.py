from playwright.sync_api import Page, sync_playwright, expect
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.dashboard_page import DashBoardPage
from pages.panel_page import PanelPage

def test_grafana(page: Page, assert_snapshot):
    # browser :- Using fixture
    # Login
    login_page = LoginPage(page)
    login_page.navigate("http://localhost:3000")
    login_page.login("admin", "admin")
        
    # ASSERT: Grafana shell is visible (from codegen)
    expect(page.get_by_role("navigation", name="Breadcrumbs")).to_be_visible()

    # Create dashboard
    home_page = HomePage(page)
    home_page.create_dashboard()

    # See if Add Visualisation is there on page
    expect(page.get_by_test_id("data-testid Create new panel button")).to_contain_text("Add visualization")
        

    #now adding a new panel
    dashboard_page = DashBoardPage(page)
    dashboard_page.add_new_panel()

    expect(page.get_by_test_id("data-testid Panel editor content")).to_be_visible()

    # Now Panel page, where we select the Timeseries visualisation 
    panel_page = PanelPage(page)

    popup = panel_page.ensure_testdata_exists()

    if popup:
        # We are now inside popup page → rebuild objects with popup context
        dashboard_page = DashBoardPage(popup)
        panel_page = PanelPage(popup)

        # Re-enter panel editor inside popup window
        dashboard_page.add_new_panel()
  
    panel_page.select_testdata_source()

    expect(panel_page.panel_editor.get_by_text("Visualization")).to_be_visible()
    # timeseries option available
    expect(panel_page.timeseries_option).to_be_visible()

    
    panel_page.select_timeseries_visualization()
    panel_page.select_query_type()

    filepath = "data/testseries.csv"
    # pasting CSV data
    panel_page.csv_file_data(filepath)

    panel_page.refresh_and_zoom()

    expect(panel_page.panel_content).to_be_visible()    
    expect(panel_page.canvas).to_be_visible()


    #use this line for first time capturing the screenshot
    # panel_page.canvas.screenshot(path="tests/screenshots/expected.png")

    #to have screenshot as reference one
    assert_snapshot(panel_page.canvas.screenshot(), name="expected.png")