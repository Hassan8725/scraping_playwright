from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.doctolib.de/urologie/deutschland?insurance_sector=private")
    page.get_by_label("Annehmen und Schließen:").click()
    page.get_by_role("link", name="Frau Dr. med. Sonja Quast").click()
    page.get_by_role("link", name="Urologische").first.click()
    page.goto("https://www.doctolib.de/urologie/neuss/sonja-quast-neuss?pid=practice-28791&agenda_ids%5B%5D=77925")
    page.get_by_text("Urologische Gemeinschaftspraxis NeussStandort Neuss ZentrumHafenstraße 68,").first.click()
    page.locator("div").filter(has_text=re.compile(r"^Abrechnungsarten Gesetzlich und privat Versicherte sowie Selbstzahlende$")).nth(1).click()
    page.locator("#skills").click()
    page.locator("#skills").get_by_role("link", name="▾ Mehr").click()
    page.locator("#skills").click()
    page.get_by_text("Karte und ZugangsinformationenUrologische Gemeinschaftspraxis NeussStandort").click()
    page.get_by_role("link", name="▾ Mehr").click()
    page.locator("div:nth-child(10) > .dl-profile-card-section").click()
    page.locator("#openings_and_contact").first.click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Website öffnen").click()
    page1 = page1_info.value
    page1.get_by_role("button", name="Alle akzeptieren").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
