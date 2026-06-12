"""
tests/test_statistics_dashboard.py

Test suite for the Statistics / Dashboard popup page.

Fixture strategy
----------------
* ``dashboard_page`` (session) – logs in once, opens the system, clicks
  Dashboard, and yields a ``StatisticsDashboardPage`` instance.  Re-used by
  all read-only verification tests → fast.

* ``stats_page`` (function) – fresh authenticated context per test; navigates
  through the system list and opens the dashboard each time.  Used for tests
  that mutate UI state (date-range changes, legend toggles).

Both fixtures are defined in conftest.py.
"""

import pytest
from playwright.sync_api import expect

# ---------------------------------------------------------------------------
# Constants shared across tests
# ---------------------------------------------------------------------------

EXPECTED_SYSTEM_NAME   = "SkyElectric Karachi Office - AIO"
EXPECTED_LOCATION      = "KARACHI"
EXPECTED_TITLE_FRAGMENT = f"Dashboard / {EXPECTED_SYSTEM_NAME}"


# ===========================================================================
# TC-DASH-001  Page load & header verification
# ===========================================================================

class TestDashboardPageLoad:
    """Verify that the dashboard page loads with all expected headings."""

    def test_page_title_contains_system_name(self, dashboard_page):
        """h1 must contain 'Dashboard / <system name>'."""
        dashboard_page.assert_page_title_contains(EXPECTED_TITLE_FRAGMENT)

    def test_solar_grid_analytics_heading_visible(self, dashboard_page):
        """'Solar & Grid Analytics' section heading must be visible."""
        dashboard_page.assert_solar_grid_heading_visible()

    def test_solar_section_visible(self, dashboard_page):
        """#solar element must be visible on the page."""
        dashboard_page.assert_solar_section_visible()

    def test_solar_vs_grid_heading_visible(self, dashboard_page):
        """'Solar vs Grid' sub-heading must be visible."""
        dashboard_page.assert_solar_vs_grid_heading_visible()

    def test_location_label_visible(self, dashboard_page):
        """System location (KARACHI) must appear on the dashboard."""
        dashboard_page.assert_location_visible(EXPECTED_LOCATION)


# ===========================================================================
# TC-DASH-002  Chart / legend content
# ===========================================================================

class TestDashboardChartContent:
    """Verify that the Solar & Grid chart renders expected legend items."""

    def test_grid_consumed_legend_present(self, dashboard_page):
        """
        The main analytics chart must contain 'Grid Consumed' in its legend.

        Note: the highcharts container id is dynamic; if it changes between
        runs the test will need the id updated.  Consider querying it
        dynamically via ``page.locator("[id^='highcharts-']")`` if flakiness
        is observed.
        """
        # Use the direct page for chart id-based assertion
        expect(
            dashboard_page._page.locator("[id^='highcharts-']").first
        ).to_contain_text("Grid Consumed")

    def test_solar_export_legend_present(self, dashboard_page):
        """'Solar Export' legend label must be present."""
        expect(dashboard_page.solar_export_label).to_be_attached()


# ===========================================================================
# TC-DASH-003  Predicted Data section
# ===========================================================================

class TestPredictedDataSection:
    """Verify the Predicted Data section and its sub-elements."""

    def test_predicted_data_label_visible(self, dashboard_page):
        """'Predicted Data' text must be visible."""
        dashboard_page.assert_predicted_data_visible()

    def test_real_vs_predicted_delta_visible(self, dashboard_page):
        """'Real vs Predicted Delta' text must be visible."""
        dashboard_page.assert_real_vs_predicted_delta_visible()

    def test_predicted_data_container_present(self, dashboard_page):
        """The app-statistics-predicteddata component must be in the DOM."""
        expect(dashboard_page.predicted_data_container).to_be_attached()


# ===========================================================================
# TC-DASH-004  Date-range picker  (function-scoped – mutates UI state)
# ===========================================================================

class TestDateRangePicker:
    """Verify calendar / date-range picker interactions."""

    def test_calendar_button_visible(self, stats_page):
        """The calendar / date-range button must be visible."""
        expect(stats_page.calendar_button).to_be_visible()

    def test_calendar_button_has_date_text(self, stats_page):
        """The calendar button label must contain a date string."""
        label = stats_page.get_current_date_range_text()
        # Expect something like "May 09, 2026 – Jun 09, 2026"
        assert "2026" in label or "2025" in label, (
            f"Calendar button label did not contain a year: '{label}'"
        )

    def test_set_to_default_resets_date_range(self, stats_page):
        """
        Clicking 'Set to Default' should restore the default date range.
        We verify the button is clickable and the dashboard remains stable
        after the reset (heading still visible).
        """
        stats_page.reset_date_range()
        stats_page.assert_solar_grid_heading_visible()

    def test_calendar_opens_on_click(self, stats_page):
        """
        Clicking the calendar button should open the date-picker overlay.
        We confirm the Set-to-Default button becomes visible (it lives inside
        the picker panel).
        """
        stats_page.open_calendar()
        expect(stats_page.set_to_default_button).to_be_visible()


# ===========================================================================
# TC-DASH-005  Solar & Grid heading interaction
# ===========================================================================

class TestSolarGridHeadingInteraction:
    """
    Clicking the 'Solar & Grid Analytics' heading should not navigate away
    or collapse the section – the heading must remain visible.
    """

    def test_heading_remains_visible_after_click(self, stats_page):
        stats_page.click_solar_grid_heading()
        stats_page.assert_solar_grid_heading_visible()

    def test_solar_section_remains_visible_after_heading_click(self, stats_page):
        stats_page.click_solar_grid_heading()
        stats_page.assert_solar_section_visible()


# ===========================================================================
# TC-DASH-006  Solar Export legend toggle  (function-scoped)
# ===========================================================================

class TestLegendToggle:
    """
    Clicking 'Solar Export' in the chart legend should toggle the series.
    We verify the element is interactive and the chart heading remains
    visible after toggling.
    """

    def test_solar_export_label_clickable(self, stats_page):
        """Solar Export label must be visible and clickable."""
        expect(stats_page.solar_export_label).to_be_visible()
        stats_page.click_solar_export_label()
        # Dashboard heading must still be present after toggle
        stats_page.assert_solar_grid_heading_visible()