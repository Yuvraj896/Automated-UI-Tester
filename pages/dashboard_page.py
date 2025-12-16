#at Dashboard page, we need to just add a new panel for this assignment

class DashBoardPage:
    def __init__(self, page):
        self.page = page

        #when we tab on new visualization
        self.new_panel = page.get_by_test_id("data-testid Create new panel button")
    
    def add_new_panel(self):
        self.new_panel.click()