from playwright.sync_api import Page, expect


class SystemPage:

    URL = "https://app.skyelectric.com/systems"

    def __init__(self, page: Page):

        self.page = page

        # Cards
        self.system_cards = page.locator(
            "app-systems-card"
        )

        # Search
        self.search_box = page.get_by_role(
            "textbox",
            name="Search"
        )

        # Filter dropdown
        self.filter_dropdown = page.locator(
            "#test3"
        )

        self.customer_details = page.locator(
            "a"
        ).filter(
            has_text="Customer Details"
        )

        self.customer_contact = page.locator(
            "a"
        ).filter(
            has_text="Customer Contact"
        ).last

        # Language controls
        # Use stable selector instead of label text
        self.language_dropdown = page.locator(
            "select"
        )

        self.system_header = page.locator(
            "app-systems-header"
        )

    # ===================================
    # Navigation
    # ===================================

    def navigate(self):

        self.page.goto(self.URL)

        self.page.wait_for_load_state(
            "networkidle"
        )

    # ===================================
    # Card validation
    # ===================================

    def verify_system_cards_visible(self):

        expect(
            self.system_cards.first
        ).to_be_visible()

        expect(
            self.system_cards.nth(1)
        ).to_be_visible()

        expect(
            self.system_cards.nth(2)
        ).to_be_visible()

    # ===================================
    # Search
    # ===================================

    def search_system(self, value):

        self.search_box.clear()

        self.search_box.fill(value)

        self.search_box.press("Enter")

    def verify_search_value(self, value):

        expect(
            self.search_box
        ).to_have_value(
            value
        )

    def verify_search_result(self, text):

        expect(
            self.page.locator(
                "app-systems-new"
            )
        ).to_contain_text(
            text
        )

    # ===================================
    # Search criteria
    # ===================================

    def select_search_criteria(
        self,
        criteria
    ):

        self.filter_dropdown.click()

        if criteria == "Customer Contact":

            self.customer_details.click()

            expect(
                self.customer_contact
            ).to_be_visible()

            self.customer_contact.click()

        else:

            option = self.page.locator(
                "a"
            ).filter(
                has_text=criteria
            ).first

            expect(
                option
            ).to_be_visible()

            option.click()

    def select_customer_contact(self):

        self.filter_dropdown.click()

        self.customer_details.click()

        expect(
            self.customer_contact
        ).to_be_visible()

        self.customer_contact.click()

    def verify_customer_contact_selected(self):

        expect(
            self.filter_dropdown
        ).to_contain_text(
            "Customer Contact"
        )

    # ===================================
    # System details
    # ===================================

    def open_system(
        self,
        system_name
    ):

        system = self.page.get_by_role(
            "link"
        ).filter(
            has_text=system_name
        ).first

        expect(
            system
        ).to_be_visible()

        system.click()

    def verify_system_name(
        self,
        name
    ):

        expect(
            self.page.get_by_role(
                "textbox"
            )
        ).to_have_value(
            name
        )

    # ===================================
    # Users tab
    # ===================================

    def open_users_tab(self):

        self.page.get_by_text(
            "Users",
            exact=True
        ).click()

    def verify_users_tab_loaded(self):

        expect(
            self.page.locator(
                "app-latest-updates"
            )
        ).to_be_visible()

    # ===================================
    # Language switch
    # ===================================

    def switch_language(
        self,
        language_code
    ):

        expect(
            self.language_dropdown
        ).to_be_visible()

        self.language_dropdown.select_option(
            language_code
        )

        self.page.wait_for_load_state(
            "networkidle"
        )

    def verify_japanese_language(self):

        expect(
            self.system_header
        ).to_contain_text(
            "システムズ"
        )

    def verify_english_language(self):

        expect(
            self.system_header
        ).to_contain_text(
            "Systems"
        )