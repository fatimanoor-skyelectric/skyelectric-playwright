from playwright.sync_api import Page, expect


class LoginPage:
    URL = "https://app.skyelectric.com/auth"

    def __init__(self, page: Page) -> None:
        self.page = page

        # Inputs
        self.username_input = page.get_by_role("textbox", name="Username Or Email Id")
        self.password_input = page.get_by_role("textbox", name="Password")

        # Buttons
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.send_email_button = page.get_by_role("button", name="Send Email")
        self.google_sign_in = page.get_by_text("Sign in with Google")

        # Links / toggles
        self.forgot_password_link = page.get_by_text("Forgot Password")
        self.remember_me_checkbox = page.locator("input[type='checkbox']")
        self.password_eye_toggle = page.locator(".icon.py-4")

        # Error container
        self.error_container = page.locator("app-login")

    # ---------------- Navigation ----------------
    def navigate(self) -> None:
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")

    # ---------------- Actions ----------------
    def fill_username(self, username: str) -> None:
        self.username_input.fill(username)

    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    def click_sign_in(self) -> None:
        self.sign_in_button.click()

    def login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.click_sign_in()

    def toggle_remember_me(self):
        self.remember_me_checkbox.click()

    def click_forgot_password(self) -> None:
        self.forgot_password_link.click()

    def submit_forgot_password(self) -> None:
        self.send_email_button.click()

    def toggle_password_visibility(self) -> None:
        self.password_eye_toggle.click()

    # ---------------- Assertions ----------------
    def expect_sign_in_disabled(self) -> None:
        expect(self.sign_in_button).to_be_disabled()

    def expect_remember_me_checked(self) -> None:
        expect(self.remember_me_checkbox).to_be_checked()

    def expect_error_contains(self, text: str) -> None:
        expect(self.error_container).to_contain_text(text)

    def expect_forgot_password_form_visible(self) -> None:
        expect(self.send_email_button).to_be_visible()

    def submit_forgot_password_email(self, email: str) -> None:
        self.fill_username(email)
        self.send_email_button.click()

    def expect_forgot_password_success_message(self) -> None:
        expect(self.error_container).to_contain_text(
            "we’ve sent you an email"
        )


    def login_with_google(self, email: str, password: str) -> None:
        """Handles Google OAuth login flow with manual 2FA approval."""

        # Open Google popup
        with self.page.expect_popup() as popup_info:
            self.google_sign_in.click()

        google_page = popup_info.value

        # Wait for popup to load
        google_page.wait_for_load_state("domcontentloaded")

        # Email step
        google_page.get_by_role(
            "textbox",
            name="Email or phone"
        ).fill(email)

        google_page.get_by_role(
            "button",
            name="Next"
        ).click()

        # Password step
        google_page.get_by_role(
            "textbox",
            name="Enter your password"
        ).wait_for(state="visible", timeout=15000)

        google_page.get_by_role(
            "textbox",
            name="Enter your password"
        ).fill(password)

        google_page.get_by_role(
            "button",
            name="Next"
        ).click()

        # -------------------------------
        # Pause here for mobile approval
        # -------------------------------
        input(
            "\nApprove the Google login from your phone "
            "then press ENTER to continue..."
        )

        # Wait until redirected back to app
        self.page.wait_for_url("**/systems**", timeout=60000)