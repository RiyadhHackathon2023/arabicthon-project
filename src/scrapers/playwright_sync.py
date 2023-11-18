from playwright.sync_api import sync_playwright

def get_paragraphs(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        divs_and_mains = page.query_selector_all("div, main")
        paragraph_list = []
        for tag in divs_and_mains:
            paragraphs = tag.query_selector_all("p")
            for paragraph in paragraphs:
                paragraph_list.append(paragraph.text_content())
        browser.close()
        paragraph_set = set(paragraph_list)
        paragraph_list = list(paragraph_set)
        paragraph_list = [s for s in paragraph_list if s.strip()]
        return paragraph_list