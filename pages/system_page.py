from playwright.sync_api import Page, expect


class SystemsPage:
    URL = "https://app.skyelectric.com/systems"

    def __init__(self, page: Page):
        self.page = page

    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    # --------------------------------------------------
    # Time Filters
    # --------------------------------------------------

    def select_last_hour(self):
        self.page.get_by_role(
            "button",
            name="Last 24 Hours"
        ).click()

        self.page.get_by_role(
            "button",
            name="Last Hour"
        ).click()

    def select_last_24_hours(self):
        self.page.get_by_role(
            "button",
            name="Last 24 Hours"
        ).click()

    # --------------------------------------------------
    # Category Filter
    # --------------------------------------------------

    def open_category_dropdown(self):
        self.page.locator(
            ".whitespace-no-wrap.flex.items-center.justify-between"
        ).first.click()

    def select_category(self, category_name: str):
        self.open_category_dropdown()

        self.page.locator(
            "a"
        ).filter(
            has_text=category_name
        ).click()

    # --------------------------------------------------
    # System Capacity
    # --------------------------------------------------

    def select_system_capacity(self):
        self.select_category("System Capacity")

    def verify_system_capacity_filter(self):
        expect(
            self.page.locator("drag-scroll")
        ).to_contain_text(
            "10 kW (3563)"
        )

        expect(
            self.page.locator("drag-scroll")
        ).to_match_aria_snapshot(
            "- text: /5\\.5 kW \\(\\d+\\)/"
        )

    # --------------------------------------------------
    # Power Company
    # --------------------------------------------------

    def select_power_company(self):
        self.select_category("Power Company")

    def verify_power_company_filter(self):
        expect(
            self.page.locator("drag-scroll")
        ).to_match_aria_snapshot(
            "- text: /IESCO \\(\\d+\\)/"
        )

        expect(
            self.page.get_by_text("LESCO (1280)")
        ).to_be_visible()

        expect(
            self.page.get_by_text("KESC (1047)")
        ).to_be_visible()

    # --------------------------------------------------
    # Battery Capacity
    # --------------------------------------------------

    def select_battery_capacity(self):
        self.select_category("Battery Capacity")

    def verify_battery_capacity_filter(self):
        expect(
            self.page.get_by_text("kWh (2347)")
        ).to_be_visible()

        expect(
            self.page.get_by_text("kWh (1046)")
        ).to_be_visible()

        expect(
            self.page.locator("drag-scroll")
        ).to_match_aria_snapshot(
            "- text: /\\d+ kWh \\(\\d+\\)/"
        )

        expect(
            self.page.locator("drag-scroll")
        ).to_contain_text(
            "5 kWh (574)"
        )

    # --------------------------------------------------
    # Date Filter
    # --------------------------------------------------

    def open_calendar(self):
        self.page.locator(
            ".icon.pointer.calendar-button"
        ).click()

    def reset_date_filter(self):
        self.open_calendar()

        self.page.get_by_role(
            "button",
            name="Set to Default"
        ).click()

    def apply_custom_date_range(self):
        self.open_calendar()

        self.page.locator(
            "#owl-dt-picker-2"
        ).get_by_text("13").click()

        self.page.locator(
            "#owl-dt-picker-3"
        ).get_by_text("23").click()

        self.page.get_by_role(
            "button",
            name="Set",
            exact=True
        ).click()

    def verify_no_results(self):
        expect(
            self.page.locator("app-systems-new")
        ).to_contain_text(
            "We couldn't find what you are looking for"
        )

        expect(
            self.page.locator("b")
        ).to_contain_text(
            "No results found."
        )

    # --------------------------------------------------
    # Language
    # --------------------------------------------------

    def change_language_to_japanese(self):
        self.page.get_by_label(
            "Select language : English"
        ).select_option("ja")

    def verify_japanese_language(self):
        expect(
            self.page.locator("app-systems-header")
        ).to_contain_text("システムズ")

    def change_language_to_english(self):
        self.page.get_by_label(
            "言語の選択 : Japanese English"
        ).select_option("en")

    # --------------------------------------------------
    # Top Navigation
    # --------------------------------------------------

    def open_pm_dashboard(self):
        self.page.get_by_role(
            "link",
            name="PM Dashboard"
        ).click()

    def open_dashboard(self):
        self.page.get_by_role(
            "link",
            name="Dashboard",
            exact=True
        ).click()

    def open_alerts(self):
        self.page.get_by_role(
            "link",
            name="Alerts"
        ).click()

    def open_releases(self):
        self.page.get_by_role(
            "link",
            name="Releases"
        ).click()

    def open_configurations(self):
        self.page.get_by_role(
            "link",
            name="Configurations"
        ).click()

    def open_crash_reports(self):
        self.page.get_by_role(
            "link",
            name="Crash Reports"
        ).click()

    def open_devices(self):
        self.page.get_by_role(
            "link",
            name="Devices"
        ).click()

    def open_users(self):
        self.page.get_by_role(
            "link",
            name="Users"
        ).click()

    def open_warehouse(self):
        self.page.get_by_role(
            "link",
            name="Warehouse"
        ).click()

    def open_ft(self):
        self.page.get_by_role(
            "link",
            name="FT"
        ).click()

    def open_systems(self):
        self.page.get_by_role(
            "link",
            name="Systems"
        ).click()