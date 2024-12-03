import json
from playwright.sync_api import sync_playwright
import time

def scrape_schools():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.meb.gov.tr/baglantilar/okullar/index.php')
        time.sleep(5)
        
        all_data = []
        has_next_page = True
        
        while has_next_page:
            schools = page.query_selector_all('tr')
            for row in schools:
                school_info = row.query_selector('td.sorting_1 a')
                if school_info:
                    school_text = school_info.text_content()
                    il, ilce, school_name = school_text.split(' - ') if len(school_text.split(' - ')) == 3 else [None, None, None]
                    school_info_link = row.query_selector('td a[href*="okulumuz_hakkinda"]')
                    school_location_link = row.query_selector('td a[href*="harita.php"]')

                    school_data = {
                        "province": il,
                        "district": ilce,
                        "schoolName": school_name,
                        "schoolInfoLink": school_info_link.get_attribute('href') if school_info_link else None,
                        "schoolLocationLink": school_location_link.get_attribute('href') if school_location_link else None
                    }
                    
                    with open('schoolsData.json', 'a', encoding='utf-8') as f:
                        json.dump(school_data, f, ensure_ascii=False, indent=2)
                        f.write(",\n")
                    
                    print(school_data)

                    if school_name == "Zonguldak Uzunmehmet Mesleki ve Teknik Anadolu Lisesi" and ilce == "MERKEZ" and il == "ZONGULDAK":
                        has_next_page = False
                        break
            
            next_button = page.query_selector('button.dt-paging-button.next')
            if next_button:
                next_button.click()
                page.wait_for_timeout(1200)
            else:
                has_next_page = False
        
        browser.close()

if __name__ == '__main__':
    scrape_schools()
