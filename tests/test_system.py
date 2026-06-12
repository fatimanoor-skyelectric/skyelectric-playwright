# # import pytest
# # from playwright.sync_api import expect
# # from pages.system_page import SystemPage


# # @pytest.fixture()
# # def systems_page(authenticated_page):
# #     page = SystemPage(authenticated_page)
# #     page.navigate()
# #     return page


# # class TestSystemsFilters:

# #     def test_last_hour_filter(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.select_last_hour()

# #     def test_system_capacity_filter(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.select_system_capacity()
# #         systems_page.verify_system_capacity_filter()

# #     def test_power_company_filter(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.select_power_company()
# #         systems_page.verify_power_company_filter()

# #     def test_battery_capacity_filter(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.select_battery_capacity()
# #         systems_page.verify_battery_capacity_filter()


# # class TestDateFilters:

# #     def test_reset_date_filter(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.reset_date_filter()

# #     def test_custom_date_range(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.apply_custom_date_range()
# #         systems_page.verify_no_results()


# # class TestLanguage:

# #     def test_change_language_to_japanese(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.change_language_to_japanese()
# #         systems_page.verify_japanese_language()

# #     def test_change_language_back_to_english(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.change_language_to_japanese()
# #         systems_page.change_language_to_english()


# # class TestNavigation:

# #     def test_dashboard_navigation(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.open_dashboard()

# #         expect(
# #             systems_page.page.get_by_role(
# #                 "heading",
# #                 name="Dashboard"
# #             )
# #         ).to_be_visible()

# #     def test_alerts_navigation(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.open_alerts()

# #         expect(
# #             systems_page.page.get_by_text(
# #                 "Alert Details"
# #             )
# #         ).to_be_visible()

# #     def test_releases_navigation(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.open_releases()

# #         expect(
# #             systems_page.page.get_by_role(
# #                 "button",
# #                 name="+Create Release"
# #             )
# #         ).to_be_visible()

# #     def test_warehouse_navigation(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.open_warehouse()

# #         expect(
# #             systems_page.page.locator(
# #                 '[id="1"]'
# #             ).get_by_text("Warehouse")
# #         ).to_be_visible()

# #     def test_ft_navigation(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.open_ft()

# #         expect(
# #             systems_page.page.get_by_text(
# #                 "BMS FT"
# #             ).first
# #         ).to_be_visible()

# #     def test_systems_navigation(
# #         self,
# #         systems_page
# #     ):
# #         systems_page.open_systems()

# #         expect(
# #             systems_page.page.locator(
# #                 '[id="1"]'
# #             ).get_by_text(
# #                 "Systems",
# #                 exact=True
# #             )
# #         ).to_be_visible()


# import pytest

# from pages.system_page import SystemPage


# @pytest.fixture()
# def systems_page(authenticated_page):
#     page = SystemPage(authenticated_page)
#     page.navigate()
#     return page


# @pytest.mark.systems
# class TestSystems:

#     def test_language_switching(self, systems_page):

#         systems_page.verify_page_loaded()

#         systems_page.change_language_to_japanese()
#         systems_page.verify_japanese_language()

#         systems_page.change_language_to_english()

#         systems_page.page.wait_for_timeout(3000)

#         print(systems_page.page.locator("body").inner_text())

#         systems_page.verify_page_loaded()
        

#     def test_city_filter(self, systems_page):

#         systems_page.select_city("ISLAMABAD (1258)")
#         systems_page.verify_city_selected("Islamabad")

#     def test_last_24_hour_filter(self, systems_page):

#         systems_page.select_last_hour()
#         systems_page.select_last_24_hours()

#     def test_custom_date_filter(self, systems_page):

#         systems_page.open_date_picker()
#         systems_page.select_custom_date_range()
#         systems_page.verify_custom_date_applied()

#     def test_category_filter(self, systems_page):

#         systems_page.open_category_dropdown()
#         systems_page.select_system_capacity()

#     def test_sorting(self, systems_page):

#         systems_page.open_sort_dropdown()
#         systems_page.sort_by_pv_production()

#     def test_advanced_search(self, systems_page):

#         systems_page.open_advanced_search()
#         systems_page.click_more()
#         systems_page.select_component_type()
#         systems_page.select_ssg_component()
#         systems_page.click_search()

import pytest
from playwright.sync_api import expect

from pages.system_page import SystemPage


@pytest.fixture()
def systems_page(authenticated_page):
    page = SystemPage(authenticated_page)
    page.navigate()
    return page

# ==================================================
# Systems Filters
# ==================================================

@pytest.mark.systems
class TestSystemsFilters:

    def test_last_hour_filter(
        self,
        systems_page
    ):
        systems_page.select_last_hour()
        systems_page.verify_last_hour()

    def test_last_24_hour_filter(
        self,
        systems_page
    ):
        systems_page.select_last_hour()
        systems_page.select_last_24_hours()

    # def test_city_filter(
    #     self,
    #     systems_page
    # ):
    #     systems_page.select_city(
    #         "ISLAMABAD"
    #     )
    #     systems_page.verify_city_selected(
    #         "Islamabad"
    #     )

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

    def test_connectivity_filter(
        self,
        systems_page
    ):
        systems_page.select_connectivity_connected_filter()
        systems_page.verify_connectivity_connected_filter()

# ==================================================
# Date Filters
# ==================================================

@pytest.mark.systems
class TestDateFilters:

    def test_reset_date_filter(
        self,
        systems_page
    ):
        systems_page.reset_date_filter()

    def test_custom_date_range_no_results(
        self,
        systems_page
    ):
        systems_page.apply_custom_date_range()
        systems_page.verify_no_results()

    # def test_custom_date_filter(
    #     self,
    #     systems_page
    # ):
    #     systems_page.open_date_picker()
    #     systems_page.select_custom_date_range()
    #     systems_page.verify_custom_date_applied()



# ==================================================
# Navigation
# ==================================================

@pytest.mark.systems
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
            ).get_by_text(
                "Warehouse"
            )
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


# ==================================================
# Sorting
# ==================================================

@pytest.mark.systems
class TestSorting:

    def test_sort_by_pv_production(
        self,
        systems_page
    ):
        systems_page.open_sort_dropdown()
        systems_page.sort_by_pv_production()

    def test_sort_by_grid_consumption(
        self,
        systems_page
    ):
        systems_page.open_sort_dropdown()
        systems_page.sort_by_grid_consumption()

    def test_sort_by_deployment_date(
        self,
        systems_page
    ):
        systems_page.open_sort_dropdown()
        systems_page.sort_by_deployment_date()


# ==================================================
# Advanced Search
# ==================================================

@pytest.mark.systems
class TestAdvancedSearch:

    def test_advanced_search(
        self,
        systems_page
    ):
        systems_page.open_advanced_search()
        systems_page.click_more()
        systems_page.select_component_type()
        systems_page.select_ssg_component()
        systems_page.click_search()



# ==================================================
# Export
# ==================================================

# @pytest.mark.systems
# class TestExport:

#     def test_export_multiple_system_users(
#         self,
#         systems_page
#     ):
#         systems_page.export_multiple_system_users()