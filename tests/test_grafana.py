from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage

#function to test if the login is correctly working (used LoginPage Object)
def test_grafana_login():
    with sync_playwright() as p:
        #open browser (don't show in screen)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login_page = LoginPage(page)
        login_page.navigate("http://localhost:3000")
        login_page.login("admin", "admin")

        # Simple assertion: check Grafana title
        page.wait_for_timeout(3000)
        assert "Grafana" in page.title()

        browser.close()