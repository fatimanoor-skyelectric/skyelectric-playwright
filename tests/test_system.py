from pages.system_page import SystemPage


class TestSystemFilters:

    def test_TC_SYSTEM_05_verify_system_cards(
        self,
        logged_in_page
    ):

        system = SystemPage(
            logged_in_page
        )

        system.verify_system_cards_visible()


    def test_TC_SYSTEM_06_search_by_system_name(
        self,
        logged_in_page
    ):

        system = SystemPage(
            logged_in_page
        )

        system.search_system(
            "Skyelectric"
        )

        system.verify_search_value(
            "Skyelectric"
        )

        system.verify_search_result(
            "SkyElectric"
        )


    def test_TC_SYSTEM_07_search_by_customer_contact(
        self,
        logged_in_page
    ):

        system = SystemPage(
            logged_in_page
        )

        system.select_search_criteria(
            "Customer Contact"
        )

        system.verify_customer_contact_selected()

        system.search_system(
            "03178508753"
        )


    def test_TC_SYSTEM_08_verify_contact_filter_selected(
        self,
        logged_in_page
    ):

        system = SystemPage(
            logged_in_page
        )

        system.select_customer_contact()

        system.verify_customer_contact_selected()


    def test_TC_SYSTEM_09_open_system_details(
        self,
        logged_in_page
    ):

        system = SystemPage(
            logged_in_page
        )

        system.search_system(
            "Skyelectric"
        )

        system.open_system(
            "SkyElectric"
        )

        system.verify_system_name(
            "SkyElectric Karachi Office - AIO"
        )


  
    def test_TC_SYSTEM_10_switch_to_japanese(
        self,
        logged_in_page
    ):

        system = SystemPage(
            logged_in_page
        )

        system.switch_language(
            "ja"
        )

        system.verify_japanese_language()


    def test_TC_SYSTEM_11_switch_back_to_english(
        self,
        logged_in_page
    ):

        system = SystemPage(
            logged_in_page
        )

        system.switch_language(
            "ja"
        )

        system.verify_japanese_language()

        system.switch_language(
            "en"
        )

        system.verify_english_language()