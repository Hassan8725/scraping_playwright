import json
from pathlib import Path


def extract_links(file_path: str) -> None:
    """Extract links form json file."""
    json_data = json.load(Path.open(file_path))

    # Extracting websites
    websites = [
        doctor["website"] for doctor in json_data if doctor["has_website"] == "Yes"
    ]

    # Save websites to a text file
    with Path.open(
        "./src/workflow/leads/olympus_lq/process_websites/website_links_v2.txt",
        "w",
    ) as file:
        for website in websites:
            file.write(website + "\n")


if __name__ == "__main__":
    path = "./src/workflow/leads/olympus_lq/playwright_scraping/doctors_data.json"
    extract_links(file_path=path)
