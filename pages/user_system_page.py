"""
pages/user_system_page.py – Page Object Model for the SkyElectric System Detail page.

Covers every major section surfaced in the Playwright codegen recording:
  • System search & selection
  • Details header assertions
  • Smart Flow panel (toggle, modal, update)
  • Navigation tab strip (Home → Components)
  • Home sub-tabs  (Grid, Solar, Battery)
  • Statistics (graph/tab filters, view types, time ranges)
  • Alerts (time filters, column header assertions)
  • Details section (Site Details, Cabinet Details, Schedule Commands, Networks)
  • Docs / Email Communication
"""

import re
from playwright.sync_api import Page, expect, Locator


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_URL = "https://app.skyelectric.com"

# The system UUID used throughout the recording
SYSTEM_UUID = "632cdff5-0733-48a5-a081-b88616b3e6ec"

SYSTEM_URL = f"{BASE_URL}/systems/{SYSTEM_UUID}"

ALERTS_COLUMNS = (
    "Alert Details",
    "Description",
    "Status",
    "Assgined To",
    "Event Time",
    "Resolved Time",
    "Updated Time",
    "Comments",
)


# ---------------------------------------------------------------------------
# Page Object
# ---------------------------------------------------------------------------

class UserSystemPage:
    """
    Encapsulates all interactions with the SkyElectric system-detail screen.

    Usage
    -----
    page_obj = UserSystemPage(page)
    page_obj.search_and_open_system("skyelectric", "Karachi SkyElectric")
    page_obj.navigate_to_tab("Statistics")
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, page: Page) -> None:
        self.page = page

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------

    def navigate_to_systems(self) -> None:
        """Go to the /systems listing page."""
        self.page.goto(f"{BASE_URL}/systems")

    def navigate_directly_to_system(self) -> None:
        """Jump straight to the system detail page (bypasses search)."""
        self.page.goto(f"{SYSTEM_URL}/")

    def navigate_to_statistics(
        self,
        *,
        start_time: int = 1_779_374_400_000,
        end_time: int = 1_779_381_600_000,
        graphs: str = "AllStats&graphs=PvStats",
        inverter_id: int = 1,
        cabinet_id: int = 1,
        view_type: str = "graphs",
    ) -> None:
        """Navigate directly to Statistics with query params."""
        url = (
            f"{SYSTEM_URL}/Statistics"
            f"?startTime={start_time}"
            f"&endTime={end_time}"
            f"&graphs={graphs}"
            f"&inverterID={inverter_id}"
            f"&cabinetID={cabinet_id}"
            f"&isTabular=false"
            f"&viewType={view_type}"
        )
        self.page.goto(url)
        self.page.wait_for_load_state(
    "networkidle"
)

    def navigate_to_alerts(
        self,
        *,
        from_date: str = "2026-05-07T11:46:50.000Z",
        to_date: str = "2026-05-21T11:46:50.000Z",
    ) -> None:
        """Navigate directly to Alerts with a preset date range."""
        url = (
            f"{SYSTEM_URL}/Alerts"
            f"?systemId={SYSTEM_UUID}"
            f"&from={from_date}"
            f"&to={to_date}"
        )
        self.page.goto(url)
        self.page.wait_for_load_state(
        "networkidle"
    )

    # ------------------------------------------------------------------
    # Search & system selection
    # ------------------------------------------------------------------

    def search_system(self, query: str) -> None:
        """Type a search term into the global search box and submit."""
        search_box = self.page.get_by_role("textbox", name="Search")
        search_box.click()
        search_box.fill(query)
        search_box.press("Enter")

    def open_system(self, link_name_pattern: str) -> None:
        system_link = self.page.get_by_role(
            "link",
            name=re.compile(
                rf"{re.escape(link_name_pattern)}.*AIO",
                re.IGNORECASE
            )
        )

        expect(system_link).to_be_visible()
        system_link.click()

    def search_and_open_system(self, query: str, link_name_pattern: str) -> None:
        """Convenience: search then click the matching system link."""
        self.search_system(query)
        self.open_system(link_name_pattern)

    
    def enable_pv_stats_graph(self):

        self.open_statistics_graph_selector()

        self.page.mouse.wheel(0, 1000)

        pv = self.page.get_by_text(
            re.compile(
                r"PV Stats",
                re.IGNORECASE
            )
        )

        expect(pv.first).to_be_visible(
            timeout=15000
        )

        pv.first.click()
    # ------------------------------------------------------------------
    # Details header assertions
    # ------------------------------------------------------------------

    @property
    def _details_header(self) -> Locator:
        return self.page.locator("details-header")

    def assert_system_config_visible(self, config_text: str = "0.0 x 6 x 5.12") -> None:
        expect(self._details_header).to_contain_text(config_text)

    def assert_header_contains(self, text: str) -> None:
        expect(self._details_header).to_contain_text(text)

    def assert_smart_flow_label_visible(self) -> None:
        expect(self._details_header).to_contain_text("Smart Flow")

    def assert_view_dashboard_visible(self) -> None:
        expect(self.page.get_by_text("View Dashboard")).to_be_visible()

    def assert_installation_date_visible(self) -> None:
        expect(self.page.get_by_text("Installation Date")).to_be_visible()

    def assert_apply_configurations_visible(self) -> None:
        expect(self.page.get_by_text("Apply Configurations")).to_be_visible()

    def assert_outage_predictions_visible(self) -> None:
        expect(self.page.get_by_text("Outage Predictions")).to_be_visible()

    def assert_all_header_elements(self) -> None:
        """Run all standard header assertions in one call."""
        self.assert_system_config_visible()
        self.assert_header_contains("Type")
        self.assert_header_contains("Customer Name")
        self.assert_header_contains("Registration:")
        self.assert_smart_flow_label_visible()
        self.assert_view_dashboard_visible()
        self.assert_installation_date_visible()
        self.assert_apply_configurations_visible()
        self.assert_outage_predictions_visible()

    # ------------------------------------------------------------------
    # Smart Flow panel
    # ------------------------------------------------------------------

    def open_smart_flow_panel(self) -> None:
        """Click the Smart Flow toggle row to expand the panel."""
        self.page.locator(".py-1.pt-1.w-4\\/12.pointer.flex").click()
        self.page.locator(".py-1.pt-1.w-4\\/12.pointer.flex").click()

    def toggle_smart_flow_switch(self) -> None:
        """Click the primary Smart Flow slider."""
        self.page.locator("span > .switch > .slider").click()

    def close_smart_flow_panel(self) -> None:
        """Click the close/collapse icon on the Smart Flow panel."""
        self.page.locator(".icon.float-right").click()

    def click_smart_flow_status_text(self) -> None:
        self.page.get_by_text("Smart Flow Status").click()

    def toggle_first_smart_flow_row(self) -> None:
        """Toggle the first row slider inside the Smart Flow dialog."""
        self.page.locator("div:nth-child(2) > .switch > .slider").first.click()

    def set_smart_flow_value(self, value: str = "50") -> None:
        """Set the numeric input inside the Smart Flow dialog."""
        inp = self.page.get_by_role("dialog").locator('input[type="text"]')
        inp.click()
        inp.dblclick()
        inp.fill(value)

    def toggle_fifth_smart_flow_row(self) -> None:
        self.page.locator("div:nth-child(5) > .w-4\\/12 > .switch > .slider").click()

    def add_smart_flow_comment(self, comment: str = "test") -> None:
        box = self.page.get_by_role(
            "textbox", name=re.compile("Type your comment here", re.IGNORECASE)
        )
        box.click()
        box.fill(comment)

    def click_smart_flow_update(self) -> None:
        self.page.get_by_role("button", name="Update").click()

    def click_smart_flow_cancel(self) -> None:
        self.page.get_by_role("button", name="Cancel").click()

    def assert_smart_flow_update_visible(self) -> None:
        expect(self.page.get_by_role("button", name="Update")).to_be_visible()

    def assert_smart_flow_cancel_visible(self) -> None:
        expect(self.page.get_by_role("button", name="Cancel")).to_be_visible()

    def assert_smart_flow_slider_visible(self) -> None:
        expect(self.page.locator("span > .switch > .slider")).to_be_visible()

    def configure_smart_flow(
        self, value: str = "50", comment: str = "test"
    ) -> None:
        """
        Full Smart Flow workflow:
          open panel → open dialog → set value → add comment → update.
        """
        self.open_smart_flow_panel()
        self.toggle_smart_flow_switch()
        self.click_smart_flow_status_text()
        self.toggle_first_smart_flow_row()
        self.set_smart_flow_value(value)
        self.toggle_fifth_smart_flow_row()
        self.add_smart_flow_comment(comment)
        self.assert_smart_flow_cancel_visible()
        self.assert_smart_flow_update_visible()
        self.click_smart_flow_update()
        self.assert_smart_flow_slider_visible()

    # ------------------------------------------------------------------
    # Tab strip navigation
    # ------------------------------------------------------------------

    _TAB_LABELS = (
        "Home",
        "Statistics",
        "Alerts",
        "Users",
        "Details",
        "Docs",
        "Email Communication",
        "System Logs",
        "Components",
    )

    def navigate_to_tab(self, tab_name: str) -> None:

        tab = self.page.locator("drag-scroll").get_by_text(
            tab_name,
            exact=True
        )

        expect(tab).to_be_visible()

        tab.click()

    def navigate_through_all_tabs(self) -> None:
        """Visit every top-level tab in sequence."""
        for tab in self._TAB_LABELS:
            self.navigate_to_tab(tab)

    def assert_tab_strip_contains_home(self) -> None:
        expect(self.page.locator("drag-scroll")).to_contain_text("Home")

    def assert_tab_strip_contains_statistics(self) -> None:
        expect(self.page.locator("drag-scroll")).to_contain_text("Statistics")

    def assert_alerts_tab_visible(self) -> None:
        expect(
            self.page.locator("drag-scroll").get_by_text("Alerts")
        ).to_be_visible()

    def assert_users_tab_visible(self) -> None:
        expect(
            self.page.locator('[id="1"]').get_by_text("Users")
        ).to_be_visible()

    # ------------------------------------------------------------------
    # Home tab – sub-sections
    # ------------------------------------------------------------------

    def click_grid_section(self):

        grid=self.page.get_by_text(
            "Grid",
            exact=True
        )

        expect(grid).to_be_visible()

        grid.scroll_into_view_if_needed()

        grid.click()


    
    def click_solar_section(self):

        # Move down to home cards area
        self.page.mouse.wheel(0, 1500)
        self.page.wait_for_timeout(1000)

        solar = self.page.get_by_text(
            re.compile(r"Generation", re.IGNORECASE)
        )

        expect(solar).to_be_visible(timeout=15000)

        solar.scroll_into_view_if_needed()
        solar.click()

    def click_battery_section(self):

        self.page.mouse.wheel(0, 1200)

        battery = self.page.get_by_text(
            re.compile(r"\bBattery\b", re.IGNORECASE)
        ).first

        expect(battery).to_be_visible(timeout=15000)

        battery.scroll_into_view_if_needed()
        battery.click()



    
    def assert_solar_visible(self):

        generation = self.page.get_by_text(
            re.compile(
                r"solar panels are generating",
                re.IGNORECASE
            )
        )

        expect(generation).to_be_visible(timeout=15000)


    def assert_battery_visible(self):

        storage = self.page.get_by_text(
            re.compile(
                r"battery is charging",
                re.IGNORECASE
            )
        )

        expect(storage).to_be_visible(timeout=15000)


    def open_grid_details_popup(self) -> None:
        self.page.locator("grid-container").get_by_role("button").filter(
            has_text=re.compile(r"^$")
        ).click()

    def open_solar_details_popup(self) -> None:
        self.page.locator("solar-container").get_by_role("button").filter(
            has_text=re.compile(r"^$")
        ).click()

    def open_battery_details_popup(self) -> None:
        self.page.locator("battery-container").get_by_role("button").click()

    # =========================
# Carousel fixes
# =========================

    def navigate_home_carousel_forward(self, steps=1):

        # Scroll repeatedly until controls appear
        for _ in range(5):

            self.page.mouse.wheel(0, 700)
            self.page.wait_for_timeout(500)

            next_btn = self.page.get_by_role(
                "button",
                name=">"
            )

            if next_btn.count() > 0:
                break

        expect(next_btn.first).to_be_visible(timeout=15000)

        for _ in range(steps):
            next_btn.first.click()
            self.page.wait_for_timeout(500)


    def navigate_home_carousel_back(self, steps=1):

        for _ in range(5):

            self.page.mouse.wheel(0, 700)
            self.page.wait_for_timeout(500)

            prev_btn = self.page.get_by_role(
                "button",
                name="<"
            )

            if prev_btn.count() > 0:
                break

        expect(prev_btn.first).to_be_visible(timeout=15000)

        for _ in range(steps):
            prev_btn.first.click()
            self.page.wait_for_timeout(500)

    # ------------------------------------------------------------------
    # Statistics tab
    # ------------------------------------------------------------------

    def open_statistics_graph_selector(self) -> None:
        self.page.locator(".mx-2.rounded").click()

    def filter_statistics_by_load(self):

        option = self.page.get_by_text(
            re.compile("^Load$", re.IGNORECASE)
        )

        expect(option).to_be_visible(timeout=10000)

        option.click()


    def filter_statistics_by_grid(self):

        option = self.page.get_by_text(
            re.compile("^Grid$", re.IGNORECASE)
        )

        expect(option).to_be_visible(timeout=10000)

        option.click()


    def filter_statistics_by_pv(self):

        option = self.page.get_by_text(
            re.compile("^PV$", re.IGNORECASE)
        )

        expect(option).to_be_visible(timeout=10000)

        option.click()


    # def filter_statistics_all_graphs(self):

    #     option = self.page.get_by_text(
    #         re.compile("All Graphs", re.IGNORECASE)
    #     )

    #     expect(option).to_be_visible(timeout=10000)

    #     option.click()
    
    def filter_statistics_all_graphs(self):

        # Open selector first if needed
        self.open_statistics_graph_selector()

        option = self.page.get_by_text(
            re.compile(r"All Graphs", re.IGNORECASE)
        ).last

        expect(option).to_be_visible(timeout=15000)

        option.scroll_into_view_if_needed()
        option.click()

    def set_statistics_view_daily(self) -> None:
        self.page.get_by_role("button", name="Daily").click()

    def set_statistics_view_weekly(self) -> None:
        self.page.get_by_role("button", name="Weekly").click()

    def set_statistics_view_monthly(self) -> None:
        self.page.get_by_role("button", name="Monthly").click()

    # ------------------------------------------------------------------
    # Alerts tab
    # ------------------------------------------------------------------

    def assert_alerts_header_columns(self):

        header=self.page.locator(
            "alerts-headers"
        )

        for column in ALERTS_COLUMNS:

            expect(header).to_contain_text(
                column
            )

    def filter_alerts_last_24_hours(self) -> None:
        self.page.get_by_role("button", name="Last 24 hours").click()

    def filter_alerts_last_7_days(self) -> None:
        self.page.get_by_role("button", name="Last 7 Days").click()

    def filter_alerts_last_14_days(self) -> None:
        self.page.get_by_role("button", name="Last 14 Days").click()

    def filter_alerts_custom(self) -> None:
        self.page.get_by_role("button", name="Custom").click()

    def reset_alerts_to_default(self):

        for _ in range(4):

            self.page.mouse.wheel(
                0,
                500
            )

            self.page.wait_for_timeout(
                500
            )

        reset_btn = self.page.get_by_text(
            re.compile(
                r"RESET",
                re.IGNORECASE
            )
        )

        expect(
            reset_btn.first
        ).to_be_visible(
            timeout=15000
        )

        reset_btn.first.click()

    def apply_all_alert_filters_in_sequence(self) -> None:
        """Cycle through every built-in time-filter button."""
        self.filter_alerts_last_24_hours()
        self.filter_alerts_last_7_days()
        self.filter_alerts_last_14_days()
        self.filter_alerts_custom()
        self.reset_alerts_to_default()

    # ------------------------------------------------------------------
    # Details section
    # ------------------------------------------------------------------

    def open_site_details(self) -> None:
        self.page.get_by_role("button", name="Site Details").click()

    def open_cabinet_details(self, cabinet_label: str = "Cabinet 1 Details") -> None:
        self.page.get_by_role("button", name=cabinet_label).click()

    def open_schedule_commands(self) -> None:
        self.page.get_by_role("button", name="Schedule Commands").click()

    def open_networks(self) -> None:
        self.page.get_by_role("button", name="Networks").click()

    def assert_details_tab_visible(self):
        expect(
            self.page.locator("drag-scroll")
            .get_by_text("Details", exact=True)
        ).to_be_visible()

    # ------------------------------------------------------------------
    # Docs & Email Communication
    # ------------------------------------------------------------------

    def open_docs(self):

        docs = self.page.locator(
            "drag-scroll"
        ).get_by_text(
            "Docs",
            exact=True
        )

        docs.click()


    def assert_docs_visible(self):
        expect(
            self.page.locator(
                "drag-scroll"
            ).get_by_text(
                "Docs",
                exact=True
            )
        ).to_be_visible()

    def open_email_communication(self) -> None:
        self.page.get_by_text("Email Communication").click()

    def assert_email_communication_visible(self) -> None:
        expect(self.page.get_by_text("Email Communication")).to_be_visible()

    def open_system_logs(self) -> None:
        self.page.get_by_text("System Logs").click()

    def open_components(self) -> None:
        self.page.get_by_text("Components", exact=True).click()

    def assert_components_visible(self) -> None:
        expect(self.page.get_by_text("Components", exact=True)).to_be_visible()