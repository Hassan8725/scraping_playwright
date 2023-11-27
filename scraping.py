from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    # Make sure to run headed.
    browser = p.chromium.launch(headless=False, slow_mo=75)
    page = browser.new_page()
    page.goto("https://www.doctolib.de/urologie/deutschland?insurance_sector=private")