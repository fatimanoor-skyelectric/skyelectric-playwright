import pytest

from pages.user_system_page import (
    SystemDetailsPage
)


SEARCH_QUERY="skyelectric"

SYSTEM_LINK="Karachi SkyElectric .. - AIO"


@pytest.fixture()
def system_page(
    authenticated_page
):

    page=SystemDetailsPage(
        authenticated_page
    )

    page.search_and_open(
        SEARCH_QUERY,
        SYSTEM_LINK
    )

    # reset language every test

    try:

        page.switch_language(
            "en"
        )

    except:

        pass

    return page


class TestSmartFlowToggle:

    def test_toggle_smart_flow_on_and_off(
        self,
        system_page
    ):

        system_page.toggle_smart_flow()

        system_page.toggle_smart_flow()


class TestStatisticsTab:

    def test_statistics_tab_opens(
        self,
        system_page
    ):

        system_page.go_to_statistics()


class TestLanguageSwitching:

    def test_switch_to_japanese_header(
        self,
        system_page
    ):

        system_page.switch_language(
            "ja"
        )

        expect(
            system_page.details_header
        ).to_contain_text(
            "スマート"
        )


class TestHomeDashboard:

    def test_first_swipe_shows_solar_distribution(
        self,
        system_page
    ):

        system_page.go_to_home()

        system_page.battery_button.click()

        expect(
            system_page.next_button
        ).to_be_visible()

        system_page.next_button.click()


    def test_battery_cabinet_clickable(
        self,
        system_page
    ):

        system_page.go_to_home()

        expect(
            system_page.battery_cabinet_img
        ).to_be_visible()

        system_page.battery_cabinet_img.click()
        