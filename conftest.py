"""
conftest.py – shared fixtures for SkyElectric Playwright tests
"""

import re

import pytest
from playwright.sync_api import (
    sync_playwright,
    Page,
    expect,
)

from pages.login_page import LoginPage
from utils.config import (
    VALID_EMAIL,
    VALID_PASSWORD,
)


# ======================================================================
# CROSS BROWSER PAGE FIXTURE
# ======================================================================

@pytest.fixture(params=["chromium", "firefox", "webkit"])
def cross_browser_page(request):

    browser_name = request.param

    with sync_playwright() as p:

        browser_launcher = getattr(p, browser_name)

        browser = browser_launcher.launch(
            headless=False,
            slow_mo=100,
        )

        context = browser.new_context(
            viewport={
                "width": 1440,
                "height": 900,
            }
        )

        page = context.new_page()

        yield page

        context.close()
        browser.close()


# ======================================================================
# NORMAL PAGE FIXTURE
# ======================================================================

@pytest.fixture(scope="function")
def page():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
        )

        context = browser.new_context(
            viewport={
                "width": 1440,
                "height": 900,
            }
        )

        page = context.new_page()

        yield page

        context.close()
        browser.close()


# ======================================================================
# AUTHENTICATED PAGE FIXTURE
# ======================================================================

@pytest.fixture(scope="function")
def authenticated_page():
    """
    Logs in programmatically on every run — no auth.json required.
    Uses the same credentials as the rest of the suite.
    """

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=300,
        )

        context = browser.new_context(
            viewport={
                "width": 1440,
                "height": 900,
            }
        )

        page = context.new_page()

        lp = LoginPage(page)
        lp.navigate()
        lp.login(VALID_EMAIL, VALID_PASSWORD)

        expect(page).to_have_url(re.compile(r"/systems"), timeout=30000)

        yield page

        context.close()
        browser.close()


# ======================================================================
# LOGIN PAGE FIXTURE
# ======================================================================

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Navigate to login page and return LoginPage instance."""

    lp = LoginPage(page)
    lp.navigate()
    return lp


# ======================================================================
# LOGGED IN PAGE FIXTURE
# ======================================================================

@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    lp = LoginPage(page)
    lp.navigate()
    lp.login(VALID_EMAIL, VALID_PASSWORD)

    expect(page).to_have_url(
        re.compile(r".*/systems.*"),
        timeout=30000
    )

    return page