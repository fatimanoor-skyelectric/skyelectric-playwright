"""
conftest.py – shared fixtures for SkyElectric Playwright tests
"""

import pytest
from playwright.sync_api import Page, Browser

from pages.login_page import LoginPage
from utils.config import VALID_EMAIL, VALID_PASSWORD


# ======================================================================
# NORMAL CONTEXT (NO SAVED SESSION)
# ======================================================================

@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    Fresh browser context with NO saved authentication.
    Used for normal login tests.
    """

    context = browser.new_context()

    yield context

    context.close()


# ======================================================================
# AUTHENTICATED CONTEXT (USES auth.json)
# ======================================================================

@pytest.fixture(scope="function")
def authenticated_context(browser: Browser):
    """
    Browser context using saved Google authentication.
    """

    context = browser.new_context(
        storage_state="auth.json"
    )

    yield context

    context.close()


# ======================================================================
# NORMAL PAGE
# ======================================================================

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()

    yield page

    page.close()


# ======================================================================
# AUTHENTICATED PAGE
# ======================================================================

@pytest.fixture(scope="function")
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()

    page.goto(
        "https://app.skyelectric.com/systems"
    )

    page.wait_for_url(
        "**/systems**",
        timeout=15000
    )

    yield page

    page.close()


# ======================================================================
# LOGIN PAGE FIXTURE
# ======================================================================

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """
    Navigate to login page and return LoginPage instance.
    """

    lp = LoginPage(page)

    lp.navigate()

    return lp


# ======================================================================
# NORMAL EMAIL/PASSWORD LOGIN
# ======================================================================

@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    """
    Logs in using normal email/password authentication.
    """

    lp = LoginPage(page)

    lp.navigate()

    lp.login(
        VALID_EMAIL,
        VALID_PASSWORD
    )

    page.wait_for_url(
        "**/systems**",
        timeout=15000
    )

    return page