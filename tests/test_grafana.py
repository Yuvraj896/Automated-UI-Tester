from playwright.sync_api import sync_playwright, expect
from pages.login_page import LoginPage

def test_grafana_login():
    with sync_playwright() as p:

        #open any browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        #create Login Page Object
        login_page = LoginPage(page)
        login_page.navigate("http://localhost:3000")
        
        #Can provide new password in this field as well
        login_page.login("admin", "admin")

        # New page to have This title
        expect(page.get_by_role("heading", name="Welcome to Grafana")).to_be_visible()

        browser.close()


