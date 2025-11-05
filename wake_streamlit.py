from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


url = "https://workout-analyser.streamlit.app"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(3000)
    content = page.content().lower()

    try:
        if "get this app back up" in content or "zzz" in content:
            print("💤 App alszik – próbálom ébreszteni...")

            # próbáljuk megkeresni a gombot több módon is
            try:
                button = page.locator("button:has-text('Yes, get this app back up!')")
                button.wait_for(state="visible", timeout=5000)
                button.click()
            except PlaywrightTimeoutError:
                # ha a fenti nem találta, próbáljuk data-testid alapján
                page.click("button[data-testid='wakeup-button-owner']", timeout=5000)

            page.wait_for_timeout(5000)
            print("✅ App felébresztve!")
        else:
            print("🚀 App már fut, nem kell ébreszteni.")

    except Exception as e:
        print(f"❌ Hiba történt az ébresztés közben: {e}")

    browser.close()
