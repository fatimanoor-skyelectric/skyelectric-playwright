import pytest
from playwright.sync_api import expect
from pages.system_page import SystemsPage


@pytest.fixture()
def systems_page(authenticated_page):
    page = SystemsPage(authenticated_page)
    page.navigate()
    return page


class TestSystemsFilters:

    def test_last_hour_filter(
        self,
        systems_page
    ):
        systems_page.select_last_hour()

    def test_system_capacity_filter(
        self,
        systems_page
    ):
        systems_page.select_system_capacity()
        systems_page.verify_system_capacity_filter()

    def test_power_company_filter(
        self,
        systems_page
    ):
        systems_page.select_power_company()
        systems_page.verify_power_company_filter()

    def test_battery_capacity_filter(
        self,
        systems_page
    ):
        systems_page.select_battery_capacity()
        systems_page.verify_battery_capacity_filter()


class TestDateFilters:

    def test_reset_date_filter(
        self,
        systems_page
    ):
        systems_page.reset_date_filter()

    def test_custom_date_range(
        self,
        systems_page
    ):
        systems_page.apply_custom_date_range()
        systems_page.verify_no_results()


class TestLanguage:

    def test_change_language_to_japanese(
        self,
        systems_page
    ):
        systems_page.change_language_to_japanese()
        systems_page.verify_japanese_language()

    def test_change_language_back_to_english(
        self,
        systems_page
    ):
        systems_page.change_language_to_japanese()
        systems_page.change_language_to_english()


class TestNavigation:

    def test_dashboard_navigation(
        self,
        systems_page
    ):
        systems_page.open_dashboard()

        expect(
            systems_page.page.get_by_role(
                "heading",
                name="Dashboard"
            )
        ).to_be_visible()

    def test_alerts_navigation(
        self,
        systems_page
    ):
        systems_page.open_alerts()

        expect(
            systems_page.page.get_by_text(
                "Alert Details"
            )
        ).to_be_visible()

    def test_releases_navigation(
        self,
        systems_page
    ):
        systems_page.open_releases()

        expect(
            systems_page.page.get_by_role(
                "button",
                name="+Create Release"
            )
        ).to_be_visible()

    def test_warehouse_navigation(
        self,
        systems_page
    ):
        systems_page.open_warehouse()

        expect(
            systems_page.page.locator(
                '[id="1"]'
            ).get_by_text("Warehouse")
        ).to_be_visible()

    def test_ft_navigation(
        self,
        systems_page
    ):
        systems_page.open_ft()

        expect(
            systems_page.page.get_by_text(
                "BMS FT"
            ).first
        ).to_be_visible()

    def test_systems_navigation(
        self,
        systems_page
    ):
        systems_page.open_systems()

        expect(
            systems_page.page.locator(
                '[id="1"]'
            ).get_by_text(
                "Systems",
                exact=True
            )
        ).to_be_visible()