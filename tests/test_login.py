import pytest
from playwright.sync_api import expect

from utils.config import (
    VALID_EMAIL,
    VALID_PASSWORD,
    INVALID_EMAIL_NOT_REGISTERED,
    INVALID_EMAIL_BAD_FORMAT,
    WRONG_PASSWORD,
)

from pages.login_page import LoginPage


# ======================================================================
# POSITIVE TEST CASES
# ======================================================================

class TestLoginPositive:

    def test_TC_LOGIN_01_valid_credentials_redirect_to_systems(
        self,
        login_page: LoginPage
    ):
        login_page.login(
            VALID_EMAIL,
            VALID_PASSWORD
        )

        login_page.page.wait_for_url(
            "**/systems**",
            timeout=15000
        )

        assert "/systems" in login_page.page.url

    def test_TC_LOGIN_02_remember_me_checkbox_can_be_checked(
        self,
        login_page: LoginPage
    ):
        login_page.toggle_remember_me()
        login_page.expect_remember_me_checked()

    def test_TC_LOGIN_03_password_visibility_toggle(
        self,
        login_page: LoginPage
    ):
        login_page.fill_password(
            VALID_PASSWORD
        )

        expect(
            login_page.password_input
        ).to_have_attribute(
            "type",
            "password"
        )

        login_page.toggle_password_visibility()

        expect(
            login_page.password_input
        ).to_have_attribute(
            "type",
            "text"
        )


# ======================================================================
# NEGATIVE TEST CASES
# ======================================================================

class TestLoginNegative:

    def test_TC_LOGIN_04_unregistered_email_shows_error(
        self,
        login_page: LoginPage
    ):
        login_page.login(
            INVALID_EMAIL_NOT_REGISTERED,
            VALID_PASSWORD
        )

        assert "/systems" not in login_page.page.url

        login_page.expect_error_contains(
            "no_user_found"
        )

    def test_TC_LOGIN_05_invalid_email_format_shows_error(
        self,
        login_page: LoginPage
    ):
        login_page.fill_username(
            INVALID_EMAIL_BAD_FORMAT
        )

        login_page.fill_password(
            VALID_PASSWORD
        )

        login_page.expect_sign_in_disabled()

    def test_TC_LOGIN_06_valid_email_wrong_password_shows_error(
        self,
        login_page: LoginPage
    ):
        login_page.login(
            VALID_EMAIL,
            WRONG_PASSWORD
        )

        expect(
            login_page.error_container
        ).to_be_visible()

        assert "/systems" not in login_page.page.url

    def test_TC_LOGIN_07_empty_username_and_password_stays_on_login(
        self,
        login_page: LoginPage
    ):
        login_page.expect_sign_in_disabled()

        assert "/auth" in login_page.page.url

    def test_TC_LOGIN_08_empty_username_keeps_SignIn_disabled(
        self,
        login_page: LoginPage
    ):
        login_page.fill_password(
            VALID_PASSWORD
        )

        login_page.expect_sign_in_disabled()

    def test_TC_LOGIN_09_empty_password_keeps_SignIn_disabled(
        self,
        login_page: LoginPage
    ):
        login_page.fill_username(
            VALID_EMAIL
        )

        login_page.expect_sign_in_disabled()


# ======================================================================
# FORGOT PASSWORD FLOW
# ======================================================================

class TestForgotPassword:

    def test_TC_LOGIN_10_forgot_password_unregistered_email_shows_error(
        self,
        login_page: LoginPage
    ):
        login_page.fill_username(
            INVALID_EMAIL_NOT_REGISTERED
        )

        login_page.click_forgot_password()

        login_page.expect_forgot_password_form_visible()

        login_page.submit_forgot_password()

        login_page.expect_error_contains(
            f"user with email {INVALID_EMAIL_NOT_REGISTERED} does not exist."
        )

    def test_TC_LOGIN_11_forgot_password_form_visible_after_clicking_link(
        self,
        login_page: LoginPage
    ):
        login_page.click_forgot_password()

        login_page.expect_forgot_password_form_visible()

        expect(
            login_page.send_email_button
        ).to_be_visible()

    def test_TC_LOGIN_12_forgot_password_valid_email_shows_confirmation(
        self,
        login_page: LoginPage
    ):
        login_page.click_forgot_password()

        login_page.expect_forgot_password_form_visible()

        login_page.submit_forgot_password_email(
            VALID_EMAIL
        )

        login_page.expect_forgot_password_success_message()


# ======================================================================
# GOOGLE AUTHENTICATION TESTS
# ======================================================================

class TestGoogleAuthentication:

    def test_TC_LOGIN_13_google_authenticated_session_redirects_to_systems(
        self,
        authenticated_page
    ):
        """
        Verifies user is already authenticated using
        saved Google session from auth.json.
        """

        assert "/systems" in authenticated_page.url