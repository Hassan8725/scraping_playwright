import json
from pathlib import Path
from time import sleep

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Make sure to run headed.
    browser = p.chromium.launch(headless=False, slow_mo=75)
    page = browser.new_page()
    page.goto("https://www.doctolib.de/urologie/deutschland?insurance_sector=private")
    page.get_by_label(
        "Annehmen und Schließen: Unsere Datenverarbeitung akzeptieren und schließen"
    ).click()

    link_selector_1 = ".dl-card-content .dl-full-width a.dl-p-doctor-result-link"
    name_selector_1 = ".dl-card-content .dl-full-width .dl-text-primary-110"
    basic_info_selector_1 = ".dl-card-content > .mt-8"

    services_selector_1 = ".dl-profile-card-content > .dl-profile-skills"
    profile_bio_selector_1 = ".dl-profile-card-content .dl-profile-bio"
    lang_selector_1 = (
        ".dl-profile-card-content > .dl-profile-row-content > div:nth-child(1)"
    )
    website_selector_1 = ".dl-profile-card-content > .dl-profile-row-content > div:nth-child(2) > div > a"

    link_selector_2 = ".dl-search-result-presentation .dl-search-result-title .dl-link"
    name_selector_2 = (
        ".dl-search-result-presentation .dl-search-result-title .dl-text-primary-110"
    )
    basic_info_selector_2 = ".dl-search-result-presentation > .ml-96"

    services_selector_2 = ".dl-profile-card-content > .dl-profile-skills"
    profile_bio_selector_2 = ".dl-profile-card-content .dl-profile-bio"
    lang_selector_2 = (
        ".dl-profile-card-content > .dl-profile-row-content > div:nth-child(1)"
    )
    website_selector_2 = ".dl-profile-card-content > .dl-profile-row-content > div:nth-child(2) > div > a"

    all_data = []

    # for _ in range(2):

    while True:  # Scraping for multiple pages
        all_link_elements = page.query_selector_all(link_selector_1)
        all_name_elements = page.query_selector_all(name_selector_1)
        all_info_elements = page.query_selector_all(basic_info_selector_1)

        if (
            len(all_link_elements) == 0
            or len(all_name_elements) == 0
            or len(all_info_elements) == 0
        ):
            all_link_elements = page.query_selector_all(link_selector_2)
            all_name_elements = page.query_selector_all(name_selector_2)
            all_info_elements = page.query_selector_all(basic_info_selector_2)

        if (
            len(all_link_elements) >= 1
            and len(all_name_elements) >= 1
            and len(all_info_elements) >= 1
        ):
            for link_elem, name_elem, info_elem in zip(
                all_link_elements, all_name_elements, all_info_elements, strict=True
            ):
                href = link_elem.evaluate("(element) => element.href")
                name = name_elem.evaluate("(element) => element.textContent")
                info = "|".join(
                    sub_div.text_content().strip()
                    for sub_div in info_elem.query_selector_all("div")
                )
                # Split the string using the '|' delimiter
                info_parts = info.split("|")

                # Remove leading/trailing spaces from each part and assign them to separate variables
                address = info_parts[0].strip() if len(info_parts) > 0 else ""
                insurance_type = info_parts[1].strip() if len(info_parts) > 1 else ""

                if href and name and info:
                    # Visit each doctor's link to extract additional information
                    doctor_page = browser.new_page()
                    doctor_page.goto(href)
                    # doctor_page.get_by_label("Annehmen und Schließen:").click()

                    all_services_elements = doctor_page.query_selector_all(
                        services_selector_1
                    )

                    all_bio_elements = doctor_page.query_selector(
                        profile_bio_selector_1
                    )
                    lang_element = doctor_page.query_selector(lang_selector_1)
                    website_element = doctor_page.query_selector(website_selector_1)

                    if (
                        len(all_services_elements) != 0
                    ):  # or len(all_bio_elements) != 0 or len(lang_element) != 0 or len(website_element) != 0:
                        all_services_elements = doctor_page.query_selector_all(
                            services_selector_2
                        )

                        all_bio_elements = doctor_page.query_selector(
                            profile_bio_selector_2
                        )
                        lang_element = doctor_page.query_selector(lang_selector_2)
                        website_element = doctor_page.query_selector(website_selector_2)

                    profile_bio = all_bio_elements.evaluate(
                        "(element) => element.textContent"
                    )

                    if lang_element:
                        languages = lang_element.evaluate(
                            "(element) => element.textContent"
                        )
                    else:
                        languages = ""

                    if website_element:
                        website = website_element.evaluate("(element) => element.href")
                        has_website = "Yes"
                    else:
                        website = ""
                        has_website = "No"

                    for elem in all_services_elements:
                        services = " | ".join(
                            sub_div.text_content().strip()
                            for sub_div in elem.query_selector_all("div")
                        )

                    # Close the doctor's page and return to the main page for scraping
                    doctor_page.close()

                    doctor_data = {
                        "name": name.strip(),
                        "address": address,
                        "insurance_type": insurance_type,
                        "profile_link": href,
                        "profile_bio": profile_bio,
                        "services": services,
                        "languages": languages,
                        "website": website,
                        "has_website": has_website,
                    }
                    all_data.append(doctor_data)

            # Scroll down to load more content
            page.mouse.wheel(delta_x=0, delta_y=5000)
            sleep(2)  # Add a delay to ensure content loading

            # Click "Next Page" button
            next_button = page.query_selector('button:has-text("Nächste Seite")')
            if next_button:
                next_button.click()
                page.wait_for_load_state("load")
                sleep(2)  # Add a delay to ensure the next page is loaded
            else:
                break  # If "Next Page" button not found, break out of loop

    # Convert collected data to JSON and save it to a file
    output_path = (
        "./src/workflow/leads/olympus_lq/playwright_scraping/doctors_data7.json"
    )
    with Path.open(output_path, "w", encoding="utf-8") as file:
        json.dump(all_data, file, indent=2, ensure_ascii=False)
