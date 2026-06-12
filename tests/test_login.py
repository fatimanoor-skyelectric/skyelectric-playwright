# import pytest
# import re
# from playwright.sync_api import expect

# from utils.config import (
#     VALID_EMAIL,
#     VALID_PASSWORD,
#     INVALID_EMAIL_NOT_REGISTERED,
#     INVALID_EMAIL_BAD_FORMAT,
#     WRONG_PASSWORD,
# )

# from pages.login_page import LoginPage


# # ======================================================================
# # POSITIVE TEST CASES
# # ======================================================================

# class TestLoginPositive:

#     # FIX 1: test_TC_LOGIN_01_cross_browser was previously nested *inside*
#     # test_TC_LOGIN_CB_01_valid_login, making it invisible to pytest.
#     # Both are now proper sibling methods of the class.

#     def test_TC_LOGIN_CB_01_valid_login(self, cross_browser_page):
#         lp = LoginPage(cross_browser_page)
#         lp.navigate()
#         lp.login(VALID_EMAIL, VALID_PASSWORD)
#         cross_browser_page.wait_for_url("**/systems**", timeout=15000)
#         assert "/systems" in cross_browser_page.url

#     def test_TC_LOGIN_01_cross_browser(self, cross_browser_page):
#         lp = LoginPage(cross_browser_page)
#         lp.navigate()
#         lp.login(VALID_EMAIL, VALID_PASSWORD)
#         cross_browser_page.wait_for_url("**/systems**", timeout=15000)
#         assert "/systems" in cross_browser_page.url

#     def test_TC_LOGIN_02_remember_me_checkbox_can_be_checked(
#         self,
#         cross_browser_page,
#     ):
#         # FIX 2: navigate() was missing — the page was blank, so the
#         # checkbox locator would never resolve.
#         lp = LoginPage(cross_browser_page)
#         lp.navigate()
#         lp.toggle_remember_me()
#         lp.expect_remember_me_checked()

#     def test_TC_LOGIN_03_password_visibility_toggle(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.fill_password(VALID_PASSWORD)

#         expect(login_page.password_input).to_have_attribute("type", "password")

#         login_page.toggle_password_visibility()

#         expect(login_page.password_input).to_have_attribute("type", "text")


# # ======================================================================
# # NEGATIVE TEST CASES
# # ======================================================================

# class TestLoginNegative:

#     def test_TC_LOGIN_04_unregistered_email_shows_error(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.login(INVALID_EMAIL_NOT_REGISTERED, VALID_PASSWORD)

#         assert "/systems" not in login_page.page.url

#         login_page.expect_error_contains("no_user_found")

#     def test_TC_LOGIN_05_invalid_email_format_shows_error(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.fill_username(INVALID_EMAIL_BAD_FORMAT)
#         login_page.fill_password(VALID_PASSWORD)
#         login_page.expect_sign_in_disabled()

#     def test_TC_LOGIN_06_valid_email_wrong_password_shows_error(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.login(VALID_EMAIL, WRONG_PASSWORD)

#         expect(login_page.error_container).to_be_visible()

#         assert "/systems" not in login_page.page.url

#     def test_TC_LOGIN_07_empty_username_and_password_stays_on_login(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.expect_sign_in_disabled()

#         assert "/auth" in login_page.page.url

#     def test_TC_LOGIN_08_empty_username_keeps_SignIn_disabled(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.fill_password(VALID_PASSWORD)
#         login_page.expect_sign_in_disabled()

#     def test_TC_LOGIN_09_empty_password_keeps_SignIn_disabled(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.fill_username(VALID_EMAIL)
#         login_page.expect_sign_in_disabled()


# # ======================================================================
# # FORGOT PASSWORD FLOW
# # ======================================================================

# class TestForgotPassword:

#     def test_TC_LOGIN_10_forgot_password_unregistered_email_shows_error(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.fill_username(INVALID_EMAIL_NOT_REGISTERED)
#         login_page.click_forgot_password()
#         login_page.expect_forgot_password_form_visible()
#         login_page.submit_forgot_password()
#         login_page.expect_error_contains(
#             f"user with email {INVALID_EMAIL_NOT_REGISTERED} does not exist."
#         )

#     def test_TC_LOGIN_11_forgot_password_form_visible_after_clicking_link(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.click_forgot_password()
#         login_page.expect_forgot_password_form_visible()
#         expect(login_page.send_email_button).to_be_visible()

#     def test_TC_LOGIN_12_forgot_password_valid_email_shows_confirmation(
#         self,
#         login_page: LoginPage,
#     ):
#         login_page.click_forgot_password()
#         login_page.expect_forgot_password_form_visible()
#         login_page.submit_forgot_password_email(VALID_EMAIL)
#         login_page.expect_forgot_password_success_message()


# # ======================================================================
# # GOOGLE AUTHENTICATION TESTS
# # ======================================================================

# # FIX 3: test_TC_LOGIN_13 was placed inside TestForgotPassword, making it
# # semantically wrong and easy to miss in reports.  It now lives in its own
# # class alongside any future Google-auth tests.

# class TestGoogleAuthentication:

#     def test_TC_LOGIN_13_google_authenticated_session_redirects_to_systems(
#         self,
#         authenticated_page,
#     ):
#         expect(authenticated_page).to_have_url(
#         re.compile(r".*/systems.*"),
#         timeout=30000
#     )


"""
test_login.py – Login screen test suite for SkyElectric.

Test ID convention : TC_LOGIN_NN_short_description
Fixtures used      : login_page (unauthenticated, function-scoped)
                     cross_browser_page (parametrised Chromium/Firefox/WebKit)
                     authenticated_page (function-scoped auth-state context)

GraphQL mutations exercised
----------------------------
- login(emailOrId, password)       → Session
- googleLogin(token)               → Session
- resetPasswordRequest(email)      → Boolean
"""

import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from utils.config import (
    INVALID_EMAIL_BAD_FORMAT,
    INVALID_EMAIL_NOT_REGISTERED,
    VALID_EMAIL,
    VALID_PASSWORD,
    WRONG_PASSWORD,
)


# ══════════════════════════════════════════════════════════════════════════════
# POSITIVE TEST CASES
# ══════════════════════════════════════════════════════════════════════════════

class TestLoginPositive:

    def test_TC_LOGIN_01_valid_login_redirects_to_systems(
        self, cross_browser_page
    ):
        """
        TC_LOGIN_01: Valid credentials → redirect to /systems.
        Runs across Chromium, Firefox, and WebKit via cross_browser_page.

        NOTE: Previously duplicated as TC_LOGIN_CB_01 — removed the duplicate.
        """
        lp = LoginPage(cross_browser_page)
        lp.navigate()
        lp.login(VALID_EMAIL, VALID_PASSWORD)
        cross_browser_page.wait_for_url("**/systems**", timeout=15_000)
        assert "/systems" in cross_browser_page.url

    def test_TC_LOGIN_02_remember_me_checkbox_can_be_checked(
        self, cross_browser_page
    ):
        """TC_LOGIN_02: Remember Me checkbox is functional."""
        lp = LoginPage(cross_browser_page)
        lp.navigate()
        lp.toggle_remember_me()
        lp.expect_remember_me_checked()

    def test_TC_LOGIN_03_password_visibility_toggle(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_03: Eye icon toggles password field between hidden and visible."""
        login_page.fill_password(VALID_PASSWORD)
        login_page.expect_password_type("password")

        login_page.toggle_password_visibility()
        login_page.expect_password_type("text")


# ══════════════════════════════════════════════════════════════════════════════
# NEGATIVE TEST CASES
# ══════════════════════════════════════════════════════════════════════════════

class TestLoginNegative:

    def test_TC_LOGIN_04_unregistered_email_shows_error(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_04: Login with unregistered email shows no_user_found error."""
        login_page.login(INVALID_EMAIL_NOT_REGISTERED, VALID_PASSWORD)

        assert "/systems" not in login_page.page.url
        login_page.expect_error_contains("no_user_found")

    def test_TC_LOGIN_05_invalid_email_format_disables_sign_in(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_05: Malformed email keeps Sign In button disabled."""
        login_page.fill_username(INVALID_EMAIL_BAD_FORMAT)
        login_page.fill_password(VALID_PASSWORD)
        login_page.expect_sign_in_disabled()

    def test_TC_LOGIN_06_valid_email_wrong_password_shows_error(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_06: Correct email with wrong password shows error, stays on /auth."""
        login_page.login(VALID_EMAIL, WRONG_PASSWORD)

        expect(login_page.error_container).to_be_visible()
        assert "/systems" not in login_page.page.url

    def test_TC_LOGIN_07_empty_fields_sign_in_disabled(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_07: Both fields empty → Sign In disabled, page stays on /auth."""
        login_page.expect_sign_in_disabled()
        assert "/auth" in login_page.page.url

    def test_TC_LOGIN_08_empty_username_keeps_sign_in_disabled(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_08: Password filled but username empty → Sign In disabled."""
        login_page.fill_password(VALID_PASSWORD)
        login_page.expect_sign_in_disabled()

    def test_TC_LOGIN_09_empty_password_keeps_sign_in_disabled(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_09: Username filled but password empty → Sign In disabled."""
        login_page.fill_username(VALID_EMAIL)
        login_page.expect_sign_in_disabled()


# ══════════════════════════════════════════════════════════════════════════════
# FORGOT PASSWORD FLOW
# ══════════════════════════════════════════════════════════════════════════════

class TestForgotPassword:

    def test_TC_LOGIN_10_forgot_password_unregistered_email_shows_error(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_10: Unregistered email on forgot-password form shows user-not-found error."""
        login_page.fill_username(INVALID_EMAIL_NOT_REGISTERED)
        login_page.click_forgot_password()
        login_page.expect_forgot_password_form_visible()
        login_page.submit_forgot_password()
        login_page.expect_error_contains(
            f"user with email {INVALID_EMAIL_NOT_REGISTERED} does not exist."
        )

    def test_TC_LOGIN_11_forgot_password_form_visible_after_clicking_link(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_11: Clicking 'Forgot Password' reveals the send-email form."""
        login_page.click_forgot_password()
        login_page.expect_forgot_password_form_visible()
        expect(login_page.send_email_button).to_be_visible()

    def test_TC_LOGIN_12_forgot_password_valid_email_shows_confirmation(
        self, login_page: LoginPage
    ):
        """TC_LOGIN_12: Valid email on forgot-password form shows confirmation message."""
        login_page.click_forgot_password()
        login_page.expect_forgot_password_form_visible()
        login_page.submit_forgot_password_email(VALID_EMAIL)
        login_page.expect_forgot_password_success_message()


# ══════════════════════════════════════════════════════════════════════════════
# GOOGLE AUTHENTICATION
# ══════════════════════════════════════════════════════════════════════════════

class TestGoogleAuthentication:

    def test_TC_LOGIN_13_google_authenticated_session_redirects_to_systems(
        self, authenticated_page
    ):
        """
        TC_LOGIN_13: Pre-authenticated session (via storage state) lands on /systems.

        This verifies the auth-state fixture works correctly; it does not
        exercise the Google OAuth popup directly.
        """
        expect(authenticated_page).to_have_url(
            re.compile(r".*/systems.*"), timeout=30_000
        )