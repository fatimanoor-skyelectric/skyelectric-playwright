
import re
from playwright.sync_api import Page, expect


class SystemPage:
    URL = "https://app.skyelectric.com/systems"

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self, page: Page):
        self.page = page

        # -----------------------------
        # Common Locators
        # -----------------------------
        self.category_dropdown = page.locator(
            ".whitespace-no-wrap.flex.items-center.justify-between"
        ).first

        self.drag_scroll = page.locator(
            "drag-scroll"
        ).first

        self.calendar_button = page.locator(
            ".icon.pointer.calendar-button"
        )

        self.systems_container = page.locator(
            "app-systems-new"
        )

    # ==================================================
    # Navigation
    # ==================================================

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def verify_page_loaded(self):
        expect(
            self.page.locator('[id="1"]').get_by_text(
                "Systems",
                exact=True
            )
        ).to_be_visible()

    def open_menu(self, menu_name: str):
        self.page.get_by_role(
            "link",
            name=menu_name,
            exact=True
        ).click()

    def open_pm_dashboard(self):
        self.open_menu("PM Dashboard")

    def open_dashboard(self):
        self.open_menu("Dashboard")

    def open_alerts(self):
        self.open_menu("Alerts")

    def open_releases(self):
        self.open_menu("Releases")

    def open_configurations(self):
        self.open_menu("Configurations")

    def open_crash_reports(self):
        self.open_menu("Crash Reports")

    def open_devices(self):
        self.open_menu("Devices")

    def open_users(self):
        self.open_menu("Users")

    def open_warehouse(self):
        self.open_menu("Warehouse")

    def open_ft(self):
        self.open_menu("FT")

    def open_systems(self):
        self.open_menu("Systems")

    # ==================================================
    # Private Helpers
    # ==================================================

    def _wait_for_page(self):
        self.page.wait_for_load_state("networkidle")

    def _open_category_dropdown(self):
        self.category_dropdown.click()

    def _open_calendar(self):
        self.calendar_button.click()

    def _category_header(self, category_name: str):
        return self.page.locator("span").filter(
            has_text=category_name
        )

    # ==================================================
    # Language
    # ==================================================

   

    # ==================================================
    # City Filters
    # ==================================================

    def select_city(self, city_text: str):
        city = self.page.locator("drag-scroll").get_by_text(
            city_text,
            exact=False
        )
        city.scroll_into_view_if_needed()
        city.click()

    def verify_city_selected(self, city_name: str):
        expect(self.systems_container).to_contain_text(city_name)

        expect(
        self.page.locator("drag-scroll")
    ).to_contain_text(
        re.compile(
            rf"{re.escape(city_name)}.*\(\d+\)",
            re.IGNORECASE
        )
    )
    # ==================================================
    # Time Filters
    # ==================================================

    def select_last_hour(self):
        self.page.get_by_role(
            "button",
            name="Last Hour"
        ).click()
        self._wait_for_page()
    
    def verify_last_hour(self):
        last_hour_selected= self.page.locator("app-shared-groupbutton")
        expect(last_hour_selected).to_contain_text("Last Hour")

    def select_last_24_hours(self):
        self.page.get_by_role(
            "button",
            name="Last 24 Hours"
        ).click()
        self._wait_for_page()

    # ==================================================
    # Connectivity Filter
    # ==================================================

    def select_connectivity_connected_filter(self):
        """Select Connectivity -> Connected filter."""

        # Step 1: Open filter dropdown
        self.page.locator("#test3").click()

        # Step 2: Expand/choose Connectivity category
        self.page.locator("a").filter(
            has_text="Connectivity Connected"
        ).click()

        # Step 3: Select Connected option
        self.page.locator("a").filter(
            has_text="Connected"
        ).nth(1).click()



    def verify_connectivity_connected_filter(self):
        expect(
            self.page.locator("#test3")
        ).to_match_aria_snapshot(
            "- text: Connected"
        )

        expect(
            self.page.locator(
                ".whitespace-no-wrap.flex.items-center.h-10"
            ).first
        ).to_be_visible()

        self.page.locator("#test3").click()

    # ==================================================
    # Date Filters
    # ==================================================

    def open_date_picker(self):
        self._open_calendar()

    def reset_date_filter(self):
        self._open_calendar()

        self.page.get_by_role(
            "button",
            name="Set to Default"
        ).click()

        self._wait_for_page()

    def apply_custom_date_range(self):
        self._open_calendar()

        calendar = self.page.locator("owl-date-time-container")

        expect(calendar.first).to_be_visible(timeout=10000)
        expect(calendar.nth(1)).to_be_visible(timeout=10000)

        from_calendar = calendar.first
        to_calendar = calendar.nth(1)

        from_calendar.get_by_text(
            "13",
            exact=True
        ).click()

        to_calendar.get_by_text(
            "23",
            exact=True
        ).click()

        set_button = self.page.get_by_role(
            "button",
            name="Set",
            exact=True
        )

        expect(set_button).to_be_visible()
        set_button.click()

        self._wait_for_page()

# .................
    def select_custom_date_range(self):
        self._open_calendar()

        self.page.locator(
            "#owl-dt-picker-0"
        ).get_by_role(
            "button",
            name="Previous month"
        ).click()

        self.page.get_by_label(
            "May 1,"
        ).get_by_text(
            "1"
        ).click()

        self.page.get_by_text(
            "2",
            exact=True
        ).nth(2).click()

        self.page.get_by_role(
            "button",
            name="Set",
            exact=True
        ).click()

        self._wait_for_page()

    def verify_custom_date_applied(self):
        expect(
        self.page.locator("body")
    ).to_contain_text("From:")

    # ==================================================
    # Category Filters
    # ==================================================

    def select_category(self, category_name: str):
        self._open_category_dropdown()

        self.page.locator(
            "a"
        ).filter(
            has_text=category_name
        ).click()

    def select_system_capacity(self):
        self.select_category(
            "System Capacity"
        )

    def select_power_company(self):
        self.select_category(
            "Power Company"
        )

    def select_battery_capacity(self):
        self.select_category(
            "Battery Capacity"
        )

    # ==================================================
    # Sorting
    # ==================================================

    def open_sort_dropdown(self):
        self.page.locator(
            ".whitespace-no-wrap.flex.items-center.h-10.mx-4 > .icon"
        ).click()

    def select_sort_option(self, option: str):
        self.page.locator(
            "a"
        ).filter(
            has_text=option
        ).click()

    def sort_by_pv_production(self):
        self.select_sort_option(
            "PV Production (High to Low)"
        )

    def sort_by_grid_consumption(self):
        self.select_sort_option(
            "Grid Consumption (High to Low)"
        )

    def sort_by_deployment_date(self):
        self.select_sort_option(
            "Deployement Date (Ascending)"
        )

  

    # ==================================================
    # Export
    # ==================================================

    def export_multiple_system_users(self):

        export_menu = self.page.locator(
            ".pointer.upload-icon .icon"
        )

        export_menu.wait_for(
            state="visible"
        )

        export_menu.click()

        option = self.page.get_by_text(
            "User with Multiple systems",
            exact=False
        )

        option.wait_for(
            state="visible"
        )

        option.click()

    # ==================================================
    # Advanced Search
    # ==================================================

    def open_advanced_search(self):
        self.page.get_by_role(
            "button",
            name="Advanced Search"
        ).click()

    def click_more(self):
        self.page.get_by_role(
            "button",
            name="More"
        ).click()

    def select_component_type(self):
        self.page.get_by_text(
            "Component Type: All"
        ).click()

    def select_ssg_component(self):
        self.page.locator(
            "a"
        ).filter(
            has_text="SSG 0.0"
        ).click()

    def click_search(self):
        self.page.get_by_role(
            "button",
            name="Search",
            exact=True
        ).click()

    # ==================================================
    # Verification Methods
    # ==================================================

    def verify_system_capacity_filter(self):
        expect(
            self._category_header(
                "System Capacity"
            )
        ).to_be_visible()

        expect(
            self.drag_scroll
        ).to_be_visible()

        expect(
            self.drag_scroll
        ).to_contain_text("kW")

    def verify_power_company_filter(self):
        expect(
            self._category_header(
                "Power Company"
            )
        ).to_be_visible()

        expect(
            self.drag_scroll
        ).to_be_visible()

        expect(
            self.drag_scroll
        ).to_contain_text("IESCO")

    def verify_battery_capacity_filter(self):
        expect(
            self._category_header(
                "Battery Capacity"
            )
        ).to_be_visible()

        expect(
            self.drag_scroll
        ).to_be_visible()

        expect(
            self.drag_scroll
        ).to_contain_text("kWh")

    def verify_no_results(self):
        expect(
            self.systems_container
        ).to_contain_text(
            "We couldn't find what you are looking for"
        )

        expect(
            self.page.locator("b")
        ).to_contain_text(
            "No results found."
        )