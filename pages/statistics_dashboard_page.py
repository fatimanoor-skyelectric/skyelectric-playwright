"""
pages/statistics_dashboard_page.py

Page-object for the Statistics / Dashboard view that opens in a popup when
the user clicks "Dashboard" from the system detail page.

URL pattern:
  https://app.skyelectric.com/statistics?systemid=...&systemname=...
"""

from __future__ import annotations

from playwright.sync_api import Page, expect


class StatisticsDashboardPage:
    """
    Encapsulates all locators and actions for the Statistics Dashboard popup.

    Parameters
    ----------
    page : Page
        The popup Page returned by ``page.expect_popup()``.
    """

    # ── URL ───────────────────────────────────────────────────────────────────
    URL_PATTERN = "/statistics"

    # ── Page-level headings / text ────────────────────────────────────────────
    PAGE_TITLE_SELECTOR          = "h1"
    SOLAR_GRID_HEADING           = "Solar & Grid Analytics"
    PREDICTED_DATA_TEXT          = "Predicted Data"
    REAL_VS_PREDICTED_DELTA_TEXT = "Real vs Predicted Delta"

    # ── Section / chart locators ──────────────────────────────────────────────
    SOLAR_SECTION_ID             = "#solar"
    SOLAR_VS_GRID_HEADING        = "Solar vs Grid"   # inside a <span>

    # ── Legend / series labels ────────────────────────────────────────────────
    SOLAR_EXPORT_LABEL           = "Solar Export"
    GRID_CONSUMED_LABEL          = "Grid Consumed"

    # ── Toolbar buttons ───────────────────────────────────────────────────────
    CALENDAR_BUTTON_PARTIAL      = "Calendar Icon"   # partial name match
    SET_TO_DEFAULT_BUTTON        = "Set to Default"

    # ── Predicted-data section ────────────────────────────────────────────────
    PREDICTED_DATA_CONTAINER     = "app-statistics-predicteddata"

    def __init__(self, page: Page) -> None:
        self._page = page

    # ── Properties (lazy locators) ────────────────────────────────────────────

    @property
    def page_heading(self):
        return self._page.locator(self.PAGE_TITLE_SELECTOR)

    @property
    def solar_grid_heading(self):
        return self._page.get_by_role("heading", name=self.SOLAR_GRID_HEADING)

    @property
    def solar_section(self):
        return self._page.locator(self.SOLAR_SECTION_ID)

    @property
    def solar_vs_grid_heading(self):
        return (
            self._page
            .locator("span")
            .filter(has_text=self.SOLAR_VS_GRID_HEADING)
            .get_by_role("heading")
        )

    @property
    def predicted_data_label(self):
        return self._page.get_by_text(self.PREDICTED_DATA_TEXT)

    @property
    def real_vs_predicted_delta_label(self):
        return self._page.get_by_text(self.REAL_VS_PREDICTED_DELTA_TEXT)

    @property
    def solar_export_label(self):
        return self._page.get_by_text(self.SOLAR_EXPORT_LABEL, exact=True)

    @property
    def calendar_button(self):
        return self._page.get_by_role(
            "button", name=self.CALENDAR_BUTTON_PARTIAL
        )

    @property
    def set_to_default_button(self):
        return self._page.get_by_role(
            "button", name=self.SET_TO_DEFAULT_BUTTON
        )

    @property
    def predicted_data_container(self):
        return self._page.locator(self.PREDICTED_DATA_CONTAINER)

    # ── Navigation / wait helpers ─────────────────────────────────────────────

    def wait_for_load(self, timeout: int = 30_000) -> None:
        """Wait until the dashboard's main heading is visible."""
        self._page.wait_for_load_state("networkidle", timeout=timeout)
        expect(self.solar_grid_heading).to_be_visible(timeout=timeout)

    # ── Assertion helpers ─────────────────────────────────────────────────────

    def assert_page_title_contains(self, text: str) -> None:
        expect(self.page_heading).to_contain_text(text)

    def assert_solar_grid_heading_visible(self) -> None:
        expect(self.solar_grid_heading).to_be_visible()

    def assert_solar_section_visible(self) -> None:
        expect(self.solar_section).to_be_visible()

    def assert_solar_vs_grid_heading_visible(self) -> None:
        expect(self.solar_vs_grid_heading).to_be_visible()

    def assert_location_visible(self, location: str) -> None:
        expect(
            self._page.get_by_text(location, exact=True)
        ).to_be_visible()

    def assert_grid_consumed_visible(self, chart_locator_id: str) -> None:
        """Assert that the 'Grid Consumed' legend item is present in a chart."""
        expect(
            self._page.locator(f"#{chart_locator_id}")
        ).to_contain_text(self.GRID_CONSUMED_LABEL)

    def assert_predicted_data_visible(self) -> None:
        expect(self.predicted_data_label).to_be_visible()

    def assert_real_vs_predicted_delta_visible(self) -> None:
        expect(self.real_vs_predicted_delta_label).to_be_visible()

    # ── Action helpers ────────────────────────────────────────────────────────

    def click_solar_grid_heading(self) -> None:
        self.solar_grid_heading.click()

    def click_solar_export_label(self) -> None:
        self.solar_export_label.click()

    def open_calendar(self) -> None:
        self.calendar_button.click()

    def reset_date_range(self) -> None:
        """
        Click 'Set to Default' to restore the dashboard's default date range.
        If the calendar picker is already open this closes it first.
        """
        self.open_calendar()
        self.set_to_default_button.click()

    def get_current_date_range_text(self) -> str:
        """Return the label text of the calendar/date-range button."""
        return self.calendar_button.inner_text()