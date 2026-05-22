"""
conftest.py – shared fixtures for SkyElectric Playwright tests.

Session-persistence strategy
------------------------------
The `authenticated_page` and `system_page` fixtures now use scope="session"
together with Playwright's storage_state API to log in ONCE per test run and
reuse the cookies/localStorage in every subsequent test:

  1. `_auth_state_file` (session) – calls LoginPage.login(), saves
     browser storage to a temp JSON file, then closes the short-lived context.

  2. `system_page` (session) – opens ONE browser + context that loads the
     saved auth state, then yields the Page for the whole session.

This means the SkyElectric login screen is visited exactly once no matter
how many tests are collected.  Individual test classes that need a clean URL
just call `page.goto(...)` themselves via UserSystemPage helpers – they still
share the authenticated session.
"""

import os
import re
import tempfile

import pytest
from playwright.sync_api import (
    sync_playwright,
    Browser,
    BrowserContext,
    Page,
    expect,
)

from pages.login_page import LoginPage
from utils.config import VALID_EMAIL, VALID_PASSWORD

BASE_URL = "https://app.skyelectric.com"


# ===========================================================================
# INTERNAL – session-level auth-state bootstrap
# ===========================================================================

@pytest.fixture(scope="session")
def _auth_state_file() -> str:
    """
    Log in once, persist the browser storage to a temp JSON file, and return
    its path.  The file lives for the duration of the pytest session.

    Returns
    -------
    str
        Absolute path to the Playwright storage-state JSON.
    """
    auth_file = tempfile.mktemp(suffix=".json", prefix="skyelectric_auth_")

    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False, slow_mo=300)

        context: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900}
        )

        page: Page = context.new_page()

        # Perform the actual login
        lp = LoginPage(page)
        lp.navigate()
        lp.login(VALID_EMAIL, VALID_PASSWORD)

        # Wait until the app has moved to the /systems URL
        expect(page).to_have_url(re.compile(r"/systems"), timeout=30_000)

        # Persist cookies + localStorage so every subsequent context can skip
        # the login screen entirely
        context.storage_state(path=auth_file)

        context.close()
        browser.close()

    yield auth_file

    # Cleanup: remove the temp auth file after the full session ends
    if os.path.exists(auth_file):
        os.remove(auth_file)


# ===========================================================================
# SESSION-SCOPED AUTHENTICATED PAGE  (the main fixture for system tests)
# ===========================================================================

@pytest.fixture(scope="session")
def system_page(_auth_state_file: str):
    """
    A single browser page that is logged in and shared across the entire test
    session.  Navigation within tests is handled by each test/page-object.

    Yields
    ------
    playwright.sync_api.Page
    """
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False, slow_mo=300)

        context: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900},
            storage_state=_auth_state_file,   # ← pre-loaded auth cookies
        )

        page: Page = context.new_page()

        # Open the app – the saved state means we land on /systems directly
        page.goto(f"{BASE_URL}/systems")
        expect(page).to_have_url(re.compile(r"/systems"), timeout=20_000)

        yield page

        context.close()
        browser.close()


# ===========================================================================
# FUNCTION-SCOPED AUTHENTICATED PAGE  (fresh context per test, still no login)
# ===========================================================================

@pytest.fixture(scope="function")
def authenticated_page(_auth_state_file: str):
    """
    Like `system_page` but function-scoped: each test gets its own browser
    context loaded from the saved auth state.  More isolation, but slower.
    Use this when a test mutates state that would affect other tests.
    """
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False, slow_mo=300)

        context: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900},
            storage_state=_auth_state_file,
        )

        page: Page = context.new_page()

        page.goto(f"{BASE_URL}/systems")
        expect(page).to_have_url(re.compile(r"/systems"), timeout=20_000)

        yield page

        context.close()
        browser.close()


# ===========================================================================
# CROSS-BROWSER PAGE (unauthenticated – uses LoginPage each time)
# ===========================================================================

@pytest.fixture(params=["chromium", "firefox", "webkit"])
def cross_browser_page(request):
    """
    Launches Chromium / Firefox / WebKit in turn.
    Each browser performs its own login because storage state is
    browser-engine-specific (cookies from Chromium are not valid in WebKit).
    """
    browser_name = request.param

    with sync_playwright() as p:
        browser_launcher = getattr(p, browser_name)
        browser: Browser = browser_launcher.launch(headless=False, slow_mo=100)

        context: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900}
        )

        page: Page = context.new_page()

        yield page

        context.close()
        browser.close()


# ===========================================================================
# PLAIN PAGE FIXTURE  (no auth – for login/negative tests)
# ===========================================================================

@pytest.fixture(scope="function")
def page():
    """
    A raw unauthenticated page.  Used for login-screen tests and any test
    that intentionally starts without a session.
    """
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False, slow_mo=500)

        context: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900}
        )

        page: Page = context.new_page()

        yield page

        context.close()
        browser.close()


# ===========================================================================
# LOGIN PAGE FIXTURE  (convenience wrapper around the plain page)
# ===========================================================================

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Navigate to the login screen and return a LoginPage instance."""
    lp = LoginPage(page)
    lp.navigate()
    return lp


# ===========================================================================
# LOGGED-IN PAGE FIXTURE  (function-scoped, performs full login each time)
# ===========================================================================

@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    """
    Logs in fresh on every test function.
    Prefer `authenticated_page` (auth-state) or `system_page` (session-shared)
    for better performance.  Keep this fixture for tests that specifically need
    to exercise the login flow itself.
    """
    lp = LoginPage(page)
    lp.navigate()
    lp.login(VALID_EMAIL, VALID_PASSWORD)

    expect(page).to_have_url(
        re.compile(r".*/systems.*"),
        timeout=30_000,
    )

    return page