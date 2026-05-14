"""
conftest.py  –  shared fixtures for SkyElectric Playwright tests
Credentials live in config.py to avoid circular imports.
"""

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from utils.config import VALID_EMAIL, VALID_PASSWORD


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Navigate to the login page and return a LoginPage instance."""
    lp = LoginPage(page)
    lp.navigate()
    return lp


@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    """Return a page already authenticated with valid credentials."""
    lp = LoginPage(page)
    lp.navigate()
    lp.login(VALID_EMAIL, VALID_PASSWORD)
    page.wait_for_url("**/systems**", timeout=15_000)
    return page