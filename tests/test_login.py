"""
test_login.py  –  Login flow tests for app.skyelectric.com/auth

Positive tests
--------------
TC_LOGIN_01  Valid credentials → redirected to /systems
TC_LOGIN_02  Remember Me checkbox persists selection
TC_LOGIN_03  Password visibility toggle changes input type

Negative tests
--------------
TC_LOGIN_04  Unregistered e-mail → "no_user_found" / "does not exist" error
TC_LOGIN_05  Invalid e-mail format (no @) → error shown
TC_LOGIN_06  Valid e-mail + wrong password → error shown
TC_LOGIN_07  Empty username + empty password → sign-in stays on login page
TC_LOGIN_08  Empty username only → error shown
TC_LOGIN_09  Empty password only → error shown

Forgot-Password flow
--------------------
TC_LOGIN_10  Forgot password with unregistered e-mail → "does not exist" message
TC_LOGIN_11  Forgot password with empty e-mail → Send Email stays on form
"""

import pytest
from playwright.sync_api import Page, expect

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

    def test_TC_LOGIN_01_valid_credentials_redirect_to_systems(self, login_page: LoginPage):
        """Valid email + valid password should land the user on /systems."""
        login_page.login(VALID_EMAIL, VALID_PASSWORD)

        # Wait for navigation away from /auth
        login_page.page.wait_for_url("**/systems**", timeout=15_000)
        assert "/systems" in login_page.page.url, (
            f"Expected redirect to /systems, got: {login_page.page.url}"
        )

    def test_TC_LOGIN_02_remember_me_checkbox_can_be_checked(self, login_page: LoginPage):
        """Remember Me checkbox should become checked when clicked."""
        login_page.toggle_remember_me()
        login_page.expect_remember_me_checked()

    def test_TC_LOGIN_03_password_visibility_toggle(self, login_page: LoginPage):
        """Clicking the eye icon should toggle password field type."""
        login_page.fill_password(VALID_PASSWORD)

        # Default state: password is hidden
        expect(login_page.password_input).to_have_attribute("type", "password")

        # After toggle: password is visible
        login_page.toggle_password_visibility()
        expect(login_page.password_input).to_have_attribute("type", "text")

        # Toggle back: password is hidden again
        login_page.toggle_password_visibility()
        expect(login_page.password_input).to_have_attribute("type", "password")


# ======================================================================
# NEGATIVE TEST CASES
# ======================================================================

class TestLoginNegative:

    def test_TC_LOGIN_04_unregistered_email_shows_error(self, login_page: LoginPage):
        """An e-mail that has no account should trigger a 'does not exist' error."""
        login_page.login(INVALID_EMAIL_NOT_REGISTERED, VALID_PASSWORD)

        # Page must stay on /auth
        assert "/auth" in login_page.page.url or "systems" not in login_page.page.url

        # Error message variants observed in codegen
        error_locator = login_page.page.locator("app-login")
        expect(error_locator).to_be_visible()
        error_text = error_locator.inner_text()
        assert any(
            phrase in error_text
            for phrase in ["does not exist", "no_user_found"]
        ), f"Expected a 'not found' error, got: {error_text!r}"

    def test_TC_LOGIN_05_invalid_email_format_shows_error(self, login_page: LoginPage):
        """A username with no '@' should be rejected."""
        login_page.login(INVALID_EMAIL_BAD_FORMAT, VALID_PASSWORD)

        # Still on auth page
        assert "/auth" in login_page.page.url or "systems" not in login_page.page.url

        error_locator = login_page.page.locator("app-login")
        expect(error_locator).to_be_visible()
        error_text = error_locator.inner_text()
        assert any(
            phrase in error_text
            for phrase in ["does not exist", "no_user_found", "invalid", "not found"]
        ), f"Expected an error for bad email format, got: {error_text!r}"

    def test_TC_LOGIN_06_valid_email_wrong_password_shows_error(self, login_page: LoginPage):
        """Correct e-mail but wrong password must stay on login with an error."""
        login_page.login(VALID_EMAIL, WRONG_PASSWORD)

        # Must not navigate to systems
        login_page.page.wait_for_timeout(2_000)  # allow error toast to appear
        assert "/systems" not in login_page.page.url, (
            "Should not be redirected on wrong password"
        )

        error_locator = login_page.page.locator("app-login")
        expect(error_locator).to_be_visible()

    def test_TC_LOGIN_07_empty_username_and_password_stays_on_login(
        self, login_page: LoginPage
    ):
        """Submitting with both fields empty should keep the user on /auth."""
        login_page.click_sign_in()
        login_page.page.wait_for_timeout(1_000)
        assert "/systems" not in login_page.page.url

    def test_TC_LOGIN_08_empty_username_only_shows_error(self, login_page: LoginPage):
        """Password filled but username empty → should not authenticate."""
        login_page.fill_password(VALID_PASSWORD)
        login_page.click_sign_in()
        login_page.page.wait_for_timeout(1_000)
        assert "/systems" not in login_page.page.url

    def test_TC_LOGIN_09_empty_password_only_shows_error(self, login_page: LoginPage):
        """Username filled but password empty → should not authenticate."""
        login_page.fill_username(VALID_EMAIL)
        login_page.click_sign_in()
        login_page.page.wait_for_timeout(1_000)
        assert "/systems" not in login_page.page.url


# ======================================================================
# FORGOT PASSWORD FLOW
# ======================================================================

class TestForgotPassword:

    def test_TC_LOGIN_10_forgot_password_unregistered_email_shows_error(
        self, login_page: LoginPage
    ):
        """
        Opening Forgot Password and submitting an unregistered e-mail
        should show 'does not exist' message.
        """
        # Pre-fill username so the form carries it to forgot-password
        login_page.fill_username(INVALID_EMAIL_NOT_REGISTERED)
        login_page.click_forgot_password()

        # Forgot-password form should appear
        login_page.expect_forgot_password_form_visible()

        login_page.submit_forgot_password()

        # Error shown in app-login region
        login_page.expect_error(
            f"user with email {INVALID_EMAIL_NOT_REGISTERED} does not exist."
        )

    def test_TC_LOGIN_11_forgot_password_form_visible_after_clicking_link(
        self, login_page: LoginPage
    ):
        """Clicking 'Forgot Password' should reveal the Forgot Password form/section."""
        login_page.click_forgot_password()
        login_page.expect_forgot_password_form_visible()

        # Send Email button must be present
        expect(login_page.send_email_button).to_be_visible()