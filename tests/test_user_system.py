"""
tests/test_user_system.py – Test suite for the SkyElectric system-detail screen.

Fixture dependency
------------------
All tests use `system_page`, which is a session-scoped fixture defined in
conftest.py.  It logs in ONCE, then every test in this file reuses the live
browser session – no repeated auth round-trips.

Test organisation
-----------------
Each class maps to one major section of the system-detail UI so pytest's
verbose output is easy to read.  Class names intentionally mirror the UI
section names seen in the tab strip.

Run subset examples
-------------------
  pytest tests/test_user_system.py -v
  pytest tests/test_user_system.py -k "smart_flow" -v
  pytest tests/test_user_system.py::TestStatistics -v
"""

import re

import pytest
from playwright.sync_api import expect

from pages.user_system_page import UserSystemPage


# ===========================================================================
# Helper – shared fixture alias
# ===========================================================================

@pytest.fixture()
def sp(system_page) -> UserSystemPage:
    """Return a UserSystemPage bound to the shared authenticated browser page."""
    return UserSystemPage(system_page)


# ===========================================================================
# 1. System search & selection
# ===========================================================================

class TestSystemSearch:
    """
    Verify the global search flow navigates to the correct system.
    These tests navigate away, so they re-search each time.
    """

    def test_search_returns_karachi_system(self, sp: UserSystemPage) -> None:
        """Search for 'skyelectric' and confirm the target system link is present."""
        sp.navigate_to_systems()
        sp.search_system("skyelectric")
        link = sp.page.get_by_role(
            "link", name=re.compile("Karachi SkyElectric", re.IGNORECASE)
        )
        expect(link.first).to_be_visible()

    def test_open_system_lands_on_detail_page(self, sp: UserSystemPage) -> None:
        """Opening the found system link navigates to the system detail URL."""
        sp.navigate_to_systems()
        sp.search_and_open_system("skyelectric", "Karachi SkyElectric")
        expect(sp.page).to_have_url(
            re.compile(r"systems/632cdff5-0733-48a5-a081-b88616b3e6ec"),
            timeout=20_000,
        )


# ===========================================================================
# 2. Details header
# ===========================================================================

class TestDetailsHeader:
    """Assertions against the persistent details-header component."""

    @pytest.fixture(autouse=True)
    def go_to_system(self, sp: UserSystemPage) -> None:
        sp.navigate_directly_to_system()

    def test_system_config_visible(self, sp: UserSystemPage) -> None:
        sp.assert_system_config_visible()

    def test_type_label_visible(self, sp: UserSystemPage) -> None:
        sp.assert_header_contains("Type")

    def test_customer_name_visible(self, sp: UserSystemPage) -> None:
        sp.assert_header_contains("Customer Name")

    def test_registration_visible(self, sp: UserSystemPage) -> None:
        sp.assert_header_contains("Registration:")

    def test_smart_flow_label_visible(self, sp: UserSystemPage) -> None:
        sp.assert_smart_flow_label_visible()

    def test_view_dashboard_button_visible(self, sp: UserSystemPage) -> None:
        sp.assert_view_dashboard_visible()

    def test_installation_date_visible(self, sp: UserSystemPage) -> None:
        sp.assert_installation_date_visible()

    def test_apply_configurations_visible(self, sp: UserSystemPage) -> None:
        sp.assert_apply_configurations_visible()

    def test_outage_predictions_visible(self, sp: UserSystemPage) -> None:
        sp.assert_outage_predictions_visible()

    def test_all_header_elements_pass(self, sp: UserSystemPage) -> None:
        """Compound assertion: all header elements present in one shot."""
        sp.assert_all_header_elements()


# ===========================================================================
# 3. Smart Flow
# ===========================================================================

class TestSmartFlow:
    """Interactions with the Smart Flow configuration panel."""

    @pytest.fixture(autouse=True)
    def go_to_system(self, sp: UserSystemPage) -> None:
        sp.navigate_directly_to_system()

    def test_smart_flow_panel_opens(self, sp: UserSystemPage) -> None:
        """Opening the Smart Flow panel reveals the toggle slider."""
        sp.open_smart_flow_panel()
        sp.assert_smart_flow_slider_visible()

    # def test_smart_flow_panel_closes(self, sp: UserSystemPage) -> None:
    #     """Closing the panel is possible after it is opened."""
    #     sp.open_smart_flow_panel()
    #     sp.toggle_smart_flow_switch()
    #     sp.close_smart_flow_panel()
    #     # After closing, re-toggle – the slider should still be accessible
    #     sp.open_smart_flow_panel()
    #     sp.assert_smart_flow_slider_visible()

    # def test_smart_flow_dialog_cancel_visible(self, sp: UserSystemPage) -> None:
    #     """The Cancel button is visible inside the Smart Flow dialog."""
    #     sp.open_smart_flow_panel()
    #     sp.toggle_smart_flow_switch()
    #     sp.click_smart_flow_status_text()
    #     sp.toggle_first_smart_flow_row()
    #     sp.assert_smart_flow_cancel_visible()
    #     sp.assert_smart_flow_update_visible()

    # def test_smart_flow_dialog_update_visible(self, sp: UserSystemPage) -> None:
    #     """The Update button is visible inside the Smart Flow dialog."""
    #     sp.open_smart_flow_panel()
    #     sp.toggle_smart_flow_switch()
    #     sp.click_smart_flow_status_text()
    #     sp.toggle_first_smart_flow_row()
    #     sp.assert_smart_flow_update_visible()

    # def test_smart_flow_full_workflow_completes(self, sp: UserSystemPage) -> None:
    #     """
    #     End-to-end: open panel, configure value, add comment, update.
    #     Slider must still be visible after the update round-trip.
    #     """
    #     sp.configure_smart_flow(value="50", comment="automated test")
    #     sp.assert_smart_flow_slider_visible()


# ===========================================================================
# 4. Tab strip navigation
# ===========================================================================

class TestTabNavigation:
    """Verify each tab in the drag-scroll strip is reachable and visible."""

    @pytest.fixture(autouse=True)
    def go_to_system(self, sp: UserSystemPage) -> None:
        sp.navigate_directly_to_system()

    def test_home_tab_visible_in_strip(self, sp: UserSystemPage) -> None:
        sp.assert_tab_strip_contains_home()

    def test_statistics_tab_visible_in_strip(self, sp: UserSystemPage) -> None:
        sp.assert_tab_strip_contains_statistics()

    def test_alerts_tab_is_visible(self, sp: UserSystemPage) -> None:
        sp.assert_alerts_tab_visible()

    def test_navigate_to_statistics(self, sp: UserSystemPage) -> None:
        sp.navigate_to_tab("Statistics")
        expect(sp.page).to_have_url(re.compile(r"Statistics"), timeout=15_000)

    def test_navigate_to_alerts(self, sp: UserSystemPage) -> None:
        sp.navigate_to_tab("Alerts")
        sp.assert_alerts_header_columns()

    def test_navigate_to_users(self, sp: UserSystemPage) -> None:
        sp.navigate_to_tab("Alerts")   # Users sub-tab is under Alerts
        sp.assert_users_tab_visible()
        sp.navigate_to_tab("Users")

    def test_navigate_to_details(self, sp: UserSystemPage) -> None:
        sp.navigate_to_tab("Details")
        sp.assert_details_tab_visible()

    def test_navigate_to_docs(self, sp: UserSystemPage) -> None:
        sp.navigate_to_tab("Docs")
        sp.assert_docs_visible()

    def test_navigate_to_email_communication(self, sp: UserSystemPage) -> None:
        sp.navigate_to_tab("Email Communication")
        sp.assert_email_communication_visible()

    def test_navigate_to_components(self, sp: UserSystemPage) -> None:
        sp.navigate_to_tab("Components")
        sp.assert_components_visible()

    def test_full_tab_traversal(self, sp: UserSystemPage) -> None:
        """Walk through every tab without error (smoke test)."""
        sp.navigate_through_all_tabs()


# ===========================================================================
# 5. Home tab – sub-sections
# ===========================================================================

class TestHomeTab:
    """Grid, Solar, Battery sub-section visibility and detail popups."""

    @pytest.fixture(autouse=True)
    def go_to_home(self, sp: UserSystemPage) -> None:
        sp.navigate_directly_to_system()

    def test_solar_section_visible(self, sp: UserSystemPage) -> None:
        sp.click_solar_section()
        sp.assert_solar_visible()

    def test_battery_section_visible(self, sp: UserSystemPage) -> None:
        sp.click_battery_section()
        sp.assert_battery_visible()

    def test_carousel_forward_navigation(self, sp: UserSystemPage) -> None:
        """Clicking > five times does not raise an error."""
        sp.navigate_home_carousel_forward(steps=5)

    def test_carousel_back_navigation(self, sp: UserSystemPage) -> None:
        """Navigate forward then back."""
        sp.navigate_home_carousel_forward(steps=3)
        sp.navigate_home_carousel_back()


# ===========================================================================
# 6. Statistics
# ===========================================================================

class TestStatistics:
    """Graph filter buttons and view-type selectors."""

    @pytest.fixture(autouse=True)
    def go_to_statistics(self, sp: UserSystemPage) -> None:
        sp.navigate_to_statistics()

    def test_filter_by_load(self, sp: UserSystemPage) -> None:
        sp.filter_statistics_by_load()

    def test_filter_by_grid(self, sp: UserSystemPage) -> None:
        sp.filter_statistics_by_grid()

    def test_filter_by_pv(self, sp: UserSystemPage) -> None:
        sp.filter_statistics_by_pv()

    def test_filter_all_graphs(self, sp: UserSystemPage) -> None:
        sp.filter_statistics_all_graphs()

    def test_view_type_daily(self, sp: UserSystemPage) -> None:
        sp.set_statistics_view_daily()

    def test_view_type_weekly(self, sp: UserSystemPage) -> None:
        sp.set_statistics_view_weekly()

    def test_view_type_monthly(self, sp: UserSystemPage) -> None:
        sp.set_statistics_view_monthly()

    def test_toggle_pv_stats_via_selector(self, sp: UserSystemPage) -> None:
        """Open the graph selector and enable PV Stats."""
        sp.open_statistics_graph_selector()
        sp.enable_pv_stats_graph()


# ===========================================================================
# 7. Alerts
# ===========================================================================

class TestAlerts:
    """Column headers and time-range filter buttons."""

    @pytest.fixture(autouse=True)
    def go_to_alerts(self, sp: UserSystemPage) -> None:
        sp.navigate_to_alerts()

    def test_alert_details_column_header_visible(self, sp: UserSystemPage) -> None:
        expect(sp.page.locator("alerts-headers")).to_contain_text("Alert Details")

    def test_all_column_headers_present(self, sp: UserSystemPage) -> None:
        sp.assert_alerts_header_columns()

    def test_filter_last_24_hours(self, sp: UserSystemPage) -> None:
        sp.filter_alerts_last_24_hours()

    def test_filter_last_7_days(self, sp: UserSystemPage) -> None:
        sp.filter_alerts_last_7_days()

    def test_filter_last_14_days(self, sp: UserSystemPage) -> None:
        sp.filter_alerts_last_14_days()

    def test_filter_custom_range(self, sp: UserSystemPage) -> None:
        sp.filter_alerts_custom()

    def test_reset_to_default_filter(self, sp: UserSystemPage) -> None:
        sp.filter_alerts_last_7_days()
        sp.reset_alerts_to_default()

    def test_all_time_filters_in_sequence(self, sp: UserSystemPage) -> None:
        """Cycle through all built-in filters – no errors expected."""
        sp.apply_all_alert_filters_in_sequence()


# ===========================================================================
# 8. Details section
# ===========================================================================

class TestDetails:
    """Site Details, Cabinet Details, Schedule Commands, Networks panels."""

    @pytest.fixture(autouse=True)
    def go_to_details(self, sp: UserSystemPage) -> None:
        sp.navigate_directly_to_system()
        sp.navigate_to_tab("Details")

    def test_site_details_panel_opens(self, sp: UserSystemPage) -> None:
        sp.open_site_details()

    def test_cabinet_details_panel_opens(self, sp: UserSystemPage) -> None:
        sp.open_cabinet_details()

    def test_schedule_commands_panel_opens(self, sp: UserSystemPage) -> None:
        sp.open_schedule_commands()

    def test_networks_panel_opens(self, sp: UserSystemPage) -> None:
        sp.open_networks()

    def test_all_detail_panels_open_in_sequence(self, sp: UserSystemPage) -> None:
        """All four detail accordion buttons are clickable without error."""
        sp.open_site_details()
        sp.open_cabinet_details()
        sp.open_schedule_commands()
        sp.open_networks()


# ===========================================================================
# 9. Docs & Email Communication
# ===========================================================================

class TestDocsAndEmail:
    """Visibility checks for the Docs and Email Communication tabs."""

    @pytest.fixture(autouse=True)
    def go_to_system(self, sp: UserSystemPage) -> None:
        sp.navigate_directly_to_system()

    def test_docs_tab_visible_and_clickable(self, sp: UserSystemPage) -> None:
        sp.open_docs()
        sp.assert_docs_visible()

    def test_email_communication_tab_visible_and_clickable(
        self, sp: UserSystemPage
    ) -> None:
        sp.open_email_communication()
        sp.assert_email_communication_visible()

    def test_system_logs_clickable(self, sp: UserSystemPage) -> None:
        sp.open_system_logs()

    def test_components_tab_visible_and_clickable(self, sp: UserSystemPage) -> None:
        sp.open_components()
        sp.assert_components_visible()