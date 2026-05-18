# scripts/check_browsers.py

from playwright.sync_api import sync_playwright

for browser_name in ["chromium", "firefox", "webkit"]:
    with sync_playwright() as p:
        try:
            browser = getattr(p, browser_name).launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            print(f"✅ {browser_name} — OK ({page.title()})")
            browser.close()
        except Exception as e:
            print(f"❌ {browser_name} — FAILED: {e}")