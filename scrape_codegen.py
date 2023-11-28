from playwright.sync_api import Playwright, sync_playwright, expect

def extract_text_and_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text(separator='\n', strip=True)
        print("Text Content:")
        print(text_content)
        
        # Extract hyperlinks (anchor text and URLs)
        links = soup.find_all('a')
        print("\nHyperlinks:")
        for link in links:
            anchor_text = link.get_text(strip=True)
            href = link.get('href')
            print(f"Anchor Text: {anchor_text}, URL: {href}")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.doctolib.de/urologie/deutschland?insurance_sector=private")
    page.get_by_label("Annehmen und Schließen:").click()
    page.locator("#search-result-9358031 > .dl-search-result-presentation > .dl-search-result-title-container > .dl-search-result-avatar").click()
    page.locator("#skills").get_by_role("link", name="▾ Mehr").click()
    page.locator(".dl-profile-card").first.click()
    page.get_by_text("Karte und ZugangsinformationenUrologe Dr. Georg Gusbeth Boschetsrieder Str. 72").click()
    page.get_by_role("link", name="▾ Mehr").click()
    page.get_by_text("ProfilLiebe Patientin, lieber").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Website öffnen").click()
    page1 = page1_info.value

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)






from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    # Make sure to run headed.
    browser = p.chromium.launch(headless=False, slow_mo=75)
    page = browser.new_page()
    page.goto("https://www.doctolib.de/urologie/deutschland?insurance_sector=private")
    page.get_by_label("Annehmen und Schließen:").click()
    #html_section = page.inner_html(selector='#main-content > div:nth-child(3) > div > div.js-dl-doctor-results > div.col-8.col-padding.search-results-col-list')
    
    first_selector = ".dl-card-content .dl-full-width a.dl-p-doctor-result-link"

    all_results = page.query_selector_all(first_selector)
    if len(all_results) == 0:
        print("sec")

        second_selector = ".dl-search-result-presentation .dl-search-result-avatar .dl-link"
        all_results = page.query_selector_all(second_selector)
    if len(all_results)>=1: 
        # found the results
        for elem in all_results:
            print(elem)
            
        # for elem in all_results: 
        #     individual_link = elem['href']
        #     print(individual_link)
    else:
        assert False, f"no results found, check your selector"
    

    #page.get_by_role("button", name="Nächste Seite").click()

    #browser.close()

    #soup = BeautifulSoup(html_section, "html.parser")

    #print(soup.find_all("dl-search-result-title"))

    # file_path = "output1.html"
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     file.write(html_section)
    # print(f"HTML content saved to {file_path}")


    # # Function call to extract text and hyperlinks from HTML
    # extract_text_and_links(file_path)
