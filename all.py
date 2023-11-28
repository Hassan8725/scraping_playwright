from playwright.sync_api import sync_playwright
from time import sleep
import json

with sync_playwright() as p:
    # Make sure to run headed.
    browser = p.chromium.launch(headless=False, slow_mo=75)
    page = browser.new_page()
    page.goto("https://www.doctolib.de/urologie/deutschland?insurance_sector=private")
    page.get_by_label("Annehmen und Schließen:").click()

    link_selector_1 = ".dl-card-content .dl-full-width a.dl-p-doctor-result-link"
    name_selector_1 = ".dl-card-content .dl-full-width .dl-text-primary-110"
    basic_info_selector_1 = ".dl-card-content > .mt-8"
    services_selector_1 = ""
    profile_bio_selector_1 = ""
    lang_website_selector_1 = ""
    
    link_selector_2 = ".dl-search-result-presentation .dl-search-result-title .dl-link"
    name_selector_2 = ".dl-search-result-presentation .dl-search-result-title .dl-text-primary-110"
    basic_info_selector_2 = ".dl-search-result-presentation > .ml-96"
    services_selector_2 = ".dl-profile-card-content > .dl-profile-skills"
    profile_bio_selector_2 = ".dl-profile-card-content .dl-profile-bio"
    lang_website_selector_2 = ".dl-profile-card-content > .dl-profile-row-content"

    all_data = []

    while True:  # Scraping for multiple pages
        all_link_elements = page.query_selector_all(link_selector_1)
        all_name_elements = page.query_selector_all(name_selector_1)
        all_info_elements = page.query_selector_all(basic_info_selector_1)

        if len(all_link_elements) == 0 or len(all_name_elements) == 0 or len(all_info_elements) == 0:
            all_link_elements = page.query_selector_all(link_selector_2)
            all_name_elements = page.query_selector_all(name_selector_2)
            all_info_elements = page.query_selector_all(basic_info_selector_2)

        if len(all_link_elements) >= 1 and len(all_name_elements) >= 1 and len(all_info_elements) >= 1:
            for link_elem, name_elem, info_elem in zip(all_link_elements, all_name_elements, all_info_elements):
                href = link_elem.evaluate('(element) => element.href')
                name = name_elem.evaluate('(element) => element.textContent')
                info = '|'.join(sub_div.text_content().strip() for sub_div in info_elem.query_selector_all('div'))

                if href and name and info:
                    doctor_data = {
                        "name": name.strip(),
                        "basic_info": info.strip(),
                        "link": href
                    }
                    all_data.append(doctor_data)

                    # Visit each doctor's link to extract additional information
                    doctor_page = browser.new_page()
                    doctor_page.goto(href)

                    # Add your logic here to extract further information from the doctor's page
                    # For example, extracting specific details, clicking elements, etc.
                    # Extract and append the desired data to the 'doctor_data' dictionary

                    # Close the doctor's page and return to the main page for scraping
                    doctor_page.close()

            # Scroll down to load more content
            page.mouse.wheel(delta_x=0, delta_y=5000)
            sleep(2)  # Add a delay to ensure content loading

            # Click "Next Page" button
            next_button = page.query_selector('button:has-text("Nächste Seite")')
            if next_button:
                next_button.click()
                page.wait_for_load_state('load')
                sleep(2)  # Add a delay to ensure the next page is loaded
            else:
                break  # If "Next Page" button not found, break out of loop

    # Convert collected data to JSON and save it to a file
    with open('doctors_data.json', 'w', encoding='utf-8') as file:
        json.dump(all_data, file, indent=2, ensure_ascii=False)
