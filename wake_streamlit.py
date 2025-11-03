from playwright.sync_api import sync_playwright

url = "https://workout-analyser.streamlit.app"  # <-- IDE írd be a saját linkedet!

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    content = page.content().lower()
    if "get this app back up" in content:
        print("App alszik – próbálom ébreszteni...")
        page.click("text=Yes, get this app back up!")
        page.wait_for_timeout(5000)
        print("✅ App felébresztve!")
    else:
        print("💤 App már fut, nem kell ébreszteni.")
    browser.close()
