"""
Page Object Model for SkyElectric Login Page
URL: https://app.skyelectric.com/auth
"""

from playwright.sync_api import Page, expect
# NOTE: no imports from conftest or tests here — keeps the POM self-contained


class LoginPage:
    URL = "https://app.skyelectric.com/auth"

    # ------------------------------------------------------------------ #
    #  Locators
    # ------------------------------------------------------------------ #
    def __init__(self, page: Page) -> None:
        self.page = page

        # --- Inputs ---
        self.username_input = page.get_by_role("textbox", name="Username Or Email Id")
        self.password_input = page.get_by_role("textbox", name="Password")

        # --- Buttons ---
        self.sign_in_button   = page.get_by_role("button", name="Sign In")
        self.send_email_button = page.get_by_role("button", name="Send Email")
        self.google_sign_in   = page.get_by_text("Sign in with Google")

        # --- Links / toggles ---
        self.forgot_password_link  = page.get_by_text("Forgot Password")
        self.remember_me_checkbox  = page.get_by_role("checkbox")
        self.password_eye_toggle   = page.locator(".icon.py-4")

        # --- Error / info messages (live region inside app-login) ---
        self.error_message = page.locator("app-login")

    # ------------------------------------------------------------------ #
    #  Navigation
    # ------------------------------------------------------------------ #
    def navigate(self) -> None:
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    # ------------------------------------------------------------------ #
    #  Actions
    # ------------------------------------------------------------------ #
    def fill_username(self, username: str) -> None:
        self.username_input.clear()
        self.username_input.fill(username)

    def fill_password(self, password: str) -> None:
        self.password_input.clear()
        self.password_input.fill(password)

    def click_sign_in(self) -> None:
        self.sign_in_button.click()

    def login(self, username: str, password: str) -> None:
        """Full login sequence."""
        self.fill_username(username)
        self.fill_password(password)
        self.click_sign_in()

    def toggle_remember_me(self) -> None:
        self.remember_me_checkbox.check()

    def click_forgot_password(self) -> None:
        self.forgot_password_link.click()

    def submit_forgot_password(self) -> None:
        self.send_email_button.click()

    def toggle_password_visibility(self) -> None:
        self.password_eye_toggle.click()

    # ------------------------------------------------------------------ #
    #  Assertions helpers
    # ------------------------------------------------------------------ #
    def expect_error(self, text: str) -> None:
        """Assert that an error containing *text* is visible in app-login."""
        expect(self.error_message).to_contain_text(text)

    def expect_no_error(self) -> None:
        """Assert that the login error area is empty / absent."""
        expect(self.error_message).not_to_contain_text("does not exist")
        expect(self.error_message).not_to_contain_text("no_user_found")

    def expect_remember_me_checked(self) -> None:
        expect(self.remember_me_checkbox).to_be_checked()

    def expect_forgot_password_form_visible(self) -> None:
        expect(self.page.locator("form")).to_contain_text("Forgot Password")