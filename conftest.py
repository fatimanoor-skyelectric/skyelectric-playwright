

"""
conftest.py – shared fixtures for SkyElectric Playwright tests.

Session-persistence strategy
------------------------------
1. `_auth_state_file` (session) – logs in ONCE, saves browser storage to a
   temp JSON file, then closes the short-lived context.

2. `system_page` (session) – ONE shared Page for the whole test run, loaded
   from the saved auth state.  Fast — no repeated logins.

3. `authenticated_page` (function) – fresh BrowserContext per test loaded from
   the same auth state.  More isolated than system_page; use when a test
   mutates shared state.

4. `systems_page` (session) – wraps `system_page` in a SystemsPage instance
   for convenience.  Add similar wrappers for other page objects below.

5. `cross_browser_page` – parametrised Chromium / Firefox / WebKit; does its
   own login each time (storage state is engine-specific).

6. `page` – raw unauthenticated page; for login-screen and negative tests.

7. `login_page` – convenience wrapper around `page` already navigated to /auth.

8. `logged_in_page` – performs a full login on every test function; prefer
   `authenticated_page` for performance unless the test exercises the login
   flow itself.
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
from pages.system_page import SystemPage
from utils.config import VALID_EMAIL, VALID_PASSWORD
from pages.statistics_dashboard_page import StatisticsDashboardPage
from pages.user_system_page import UserSystemPage
from pages.statistics_dashboard_page import (
    StatisticsDashboardPage
)

from pages.user_system_page import (
    UserSystemPage
)

BASE_URL = "https://app.skyelectric.com"
SEARCH_QUERY = "skyelectric"
SYSTEM_LINK = "Karachi SkyElectric Karachi"

# ──────────────────────────────────────────────────────────────────────────────
# INTERNAL – session-level auth-state bootstrap
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def _auth_state_file() -> str:
    """
    Log in once, persist the browser storage to a temp JSON file, and return
    its path.  The file lives for the duration of the pytest session.
    """
    auth_file = tempfile.mktemp(suffix=".json", prefix="skyelectric_auth_")

    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False, slow_mo=300)
        context: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900}
        )
        page: Page = context.new_page()

        lp = LoginPage(page)
        lp.navigate()
        lp.login(VALID_EMAIL, VALID_PASSWORD)

        expect(page).to_have_url(re.compile(r"/systems"), timeout=30_000)

        context.storage_state(path=auth_file)
        context.close()
        browser.close()

    yield auth_file

    if os.path.exists(auth_file):
        os.remove(auth_file)


# ──────────────────────────────────────────────────────────────────────────────
# SESSION-SCOPED AUTHENTICATED PAGE  (shared across the whole session)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def system_page(_auth_state_file: str):
    """
    A single authenticated browser page shared across the entire test session.
    Individual tests navigate via their page-object helpers.
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


# ──────────────────────────────────────────────────────────────────────────────
# PAGE-OBJECT WRAPPERS (session-scoped; add one for each new page object)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def systems_page(system_page: Page) -> SystemPage:
    """Ready-to-use SystemsPage instance backed by the shared session page."""
    return SystemPage(system_page)


# ──────────────────────────────────────────────────────────────────────────────
# FUNCTION-SCOPED AUTHENTICATED PAGE  (isolated context per test)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def authenticated_page(_auth_state_file: str):
    """
    Each test gets its own BrowserContext loaded from the saved auth state.
    Use when the test mutates UI state that would affect other tests.
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


# ──────────────────────────────────────────────────────────────────────────────
# CROSS-BROWSER PAGE  (unauthenticated – logs in each time)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(params=["chromium", "firefox", "webkit"])
def cross_browser_page(request):
    """
    Launches Chromium, Firefox, and WebKit in turn.
    Each performs its own login since storage state is engine-specific.
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


# ──────────────────────────────────────────────────────────────────────────────
# PLAIN PAGE FIXTURE  (no auth – for login / negative tests)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page():
    """
    A raw unauthenticated page.
    Used for login-screen tests and any test that intentionally starts without
    a session.
    """
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        context: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900}
        )
        page: Page = context.new_page()

        yield page

        context.close()
        browser.close()


# ──────────────────────────────────────────────────────────────────────────────
# CONVENIENCE FIXTURES
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Navigate to the login screen and return a LoginPage instance."""
    lp = LoginPage(page)
    lp.navigate()
    return lp


@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    """
    Logs in fresh on every test function.

    Prefer `authenticated_page` or `system_page` for performance.
    Keep this for tests that need to exercise the login flow itself.
    """
    lp = LoginPage(page)
    lp.navigate()
    lp.login(VALID_EMAIL, VALID_PASSWORD)

    expect(page).to_have_url(re.compile(r".*/systems.*"), timeout=30_000)

    return page



@pytest.fixture(scope="session")
def dashboard_page(_auth_state_file):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            storage_state=_auth_state_file
        )

        page = context.new_page()

        page.goto("https://app.skyelectric.com/systems")

        system = UserSystemPage(page)
                # --------------------------------------------------
        # Search system ONCE
        # --------------------------------------------------

        system.search_system("skyelectric")

        page.get_by_role(
            "link",
            name="Karachi SkyElectric Karachi"
        ).click()

        expect(
            page.locator("details-header")
        ).to_contain_text("Dashboard")

        # --------------------------------------------------
        # Open dashboard ONCE
        # --------------------------------------------------

        with page.expect_popup() as popup:

            page.locator("[id='1']").get_by_text(
                "Dashboard",
                exact=True
            ).click()

        dashboard_popup = popup.value

        dashboard_popup.wait_for_load_state()

        dashboard = StatisticsDashboardPage(
            dashboard_popup
        )

        yield dashboard

        context.close()
        browser.close()




# ──────────────────────────────────────────────────────────────────────────────
# STATISTICS DASHBOARD FIXTURES
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def stats_page(authenticated_page):

    system = UserSystemPage(
        authenticated_page
    )

    system.search_and_open_system(
        "skyelectric",
        "Karachi SkyElectric"
    )

    system.assert_view_dashboard_visible()

    return system.open_dashboard()


# """
# conftest.py – shared fixtures for SkyElectric Playwright tests.

# Session-persistence strategy
# ------------------------------
# The `authenticated_page` and `system_page` fixtures now use scope="session"
# together with Playwright's storage_state API to log in ONCE per test run and
# reuse the cookies/localStorage in every subsequent test:

#   1. `_auth_state_file` (session) – calls LoginPage.login(), saves
#      browser storage to a temp JSON file, then closes the short-lived context.

#   2. `system_page` (session) – opens ONE browser + context that loads the
#      saved auth state, then yields the Page for the whole session.

# This means the SkyElectric login screen is visited exactly once no matter
# how many tests are collected.  Individual test classes that need a clean URL
# just call `page.goto(...)` themselves via UserSystemPage helpers – they still
# share the authenticated session.
# """

# import os
# import re
# import tempfile

# import pytest
# from playwright.sync_api import (
#     sync_playwright,
#     Browser,
#     BrowserContext,
#     Page,
#     expect,
# )

# from pages.login_page import LoginPage
# from utils.config import VALID_EMAIL, VALID_PASSWORD

# BASE_URL = "https://app.skyelectric.com"


# # ===========================================================================
# # INTERNAL – session-level auth-state bootstrap
# # ===========================================================================

# @pytest.fixture(scope="session")
# def _auth_state_file() -> str:
#     """
#     Log in once, persist the browser storage to a temp JSON file, and return
#     its path.  The file lives for the duration of the pytest session.

#     Returns
#     -------
#     str
#         Absolute path to the Playwright storage-state JSON.
#     """
#     auth_file = tempfile.mktemp(suffix=".json", prefix="skyelectric_auth_")

#     with sync_playwright() as p:
#         browser: Browser = p.chromium.launch(headless=False, slow_mo=300)

#         context: BrowserContext = browser.new_context(
#             viewport={"width": 1440, "height": 900}
#         )

#         page: Page = context.new_page()

#         # Perform the actual login
#         lp = LoginPage(page)
#         lp.navigate()
#         lp.login(VALID_EMAIL, VALID_PASSWORD)

#         # Wait until the app has moved to the /systems URL
#         expect(page).to_have_url(re.compile(r"/systems"), timeout=30_000)

#         # Persist cookies + localStorage so every subsequent context can skip
#         # the login screen entirely
#         context.storage_state(path=auth_file)

#         context.close()
#         browser.close()

#     yield auth_file

#     # Cleanup: remove the temp auth file after the full session ends
#     if os.path.exists(auth_file):
#         os.remove(auth_file)


# # ===========================================================================
# # SESSION-SCOPED AUTHENTICATED PAGE  (the main fixture for system tests)
# # ===========================================================================

# @pytest.fixture(scope="session")
# def system_page(_auth_state_file: str):
#     """
#     A single browser page that is logged in and shared across the entire test
#     session.  Navigation within tests is handled by each test/page-object.

#     Yields
#     ------
#     playwright.sync_api.Page
#     """
#     with sync_playwright() as p:
#         browser: Browser = p.chromium.launch(headless=False, slow_mo=300)

#         context: BrowserContext = browser.new_context(
#             viewport={"width": 1440, "height": 900},
#             storage_state=_auth_state_file,   # ← pre-loaded auth cookies
#         )

#         page: Page = context.new_page()

#         # Open the app – the saved state means we land on /systems directly
#         page.goto(f"{BASE_URL}/systems")
#         expect(page).to_have_url(re.compile(r"/systems"), timeout=20_000)

#         yield page

#         context.close()
#         browser.close()


# # ===========================================================================
# # FUNCTION-SCOPED AUTHENTICATED PAGE  (fresh context per test, still no login)
# # ===========================================================================

# @pytest.fixture(scope="function")
# def authenticated_page(_auth_state_file: str):
#     """
#     Like `system_page` but function-scoped: each test gets its own browser
#     context loaded from the saved auth state.  More isolation, but slower.
#     Use this when a test mutates state that would affect other tests.
#     """
#     with sync_playwright() as p:
#         browser: Browser = p.chromium.launch(headless=False, slow_mo=300)

#         context: BrowserContext = browser.new_context(
#             viewport={"width": 1440, "height": 900},
#             storage_state=_auth_state_file,
#         )

#         page: Page = context.new_page()

#         page.goto(f"{BASE_URL}/systems")
#         expect(page).to_have_url(re.compile(r"/systems"), timeout=20_000)

#         yield page

#         context.close()
#         browser.close()


# # ===========================================================================
# # CROSS-BROWSER PAGE (unauthenticated – uses LoginPage each time)
# # ===========================================================================

# @pytest.fixture(params=["chromium", "firefox", "webkit"])
# def cross_browser_page(request):
#     """
#     Launches Chromium / Firefox / WebKit in turn.
#     Each browser performs its own login because storage state is
#     browser-engine-specific (cookies from Chromium are not valid in WebKit).
#     """
#     browser_name = request.param

#     with sync_playwright() as p:
#         browser_launcher = getattr(p, browser_name)
#         browser: Browser = browser_launcher.launch(headless=False, slow_mo=100)

#         context: BrowserContext = browser.new_context(
#             viewport={"width": 1440, "height": 900}
#         )

#         page: Page = context.new_page()

#         yield page

#         context.close()
#         browser.close()


# # ===========================================================================
# # PLAIN PAGE FIXTURE  (no auth – for login/negative tests)
# # ===========================================================================

# @pytest.fixture(scope="function")
# def page():
#     """
#     A raw unauthenticated page.  Used for login-screen tests and any test
#     that intentionally starts without a session.
#     """
#     with sync_playwright() as p:
#         browser: Browser = p.chromium.launch(headless=False, slow_mo=500)

#         context: BrowserContext = browser.new_context(
#             viewport={"width": 1440, "height": 900}
#         )

#         page: Page = context.new_page()

#         yield page

#         context.close()
#         browser.close()


# # ===========================================================================
# # LOGIN PAGE FIXTURE  (convenience wrapper around the plain page)
# # ===========================================================================

# @pytest.fixture(scope="function")
# def login_page(page: Page) -> LoginPage:
#     """Navigate to the login screen and return a LoginPage instance."""
#     lp = LoginPage(page)
#     lp.navigate()
#     return lp


# # ===========================================================================
# # LOGGED-IN PAGE FIXTURE  (function-scoped, performs full login each time)
# # ===========================================================================

# @pytest.fixture(scope="function")
# def logged_in_page(page: Page) -> Page:
#     """
#     Logs in fresh on every test function.
#     Prefer `authenticated_page` (auth-state) or `system_page` (session-shared)
#     for better performance.  Keep this fixture for tests that specifically need
#     to exercise the login flow itself.
#     """
#     lp = LoginPage(page)
#     lp.navigate()
#     lp.login(VALID_EMAIL, VALID_PASSWORD)

#     expect(page).to_have_url(
#         re.compile(r".*/systems.*"),
#         timeout=30_000,
#     )

#     return page

