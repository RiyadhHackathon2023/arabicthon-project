# Import the asyncio and playwright libraries
import asyncio
from playwright.async_api import async_playwright

# Define an async function to scrape a website
async def get_paragraphs(url):
    # Create an async context manager for playwright
    async with async_playwright() as p:
        # Launch a chromium browser in headless mode
        browser = await p.chromium.launch(headless=True)
        # Create a new browser context
        context = await browser.new_context()
        # Create a new page
        page = await context.new_page()
        # Go to the website URL
        await page.goto(url)
        # Find all the <div> and <main> tags in the HTML document
        divs_and_mains = await page.query_selector_all("div, main")
        # Create an empty list to store the paragraph texts
        paragraph_list = []
        # Loop through each <div> or <main> tag
        for tag in divs_and_mains:
            # Find all the <p> tags inside the tag
            paragraphs = await tag.query_selector_all("p")
            # Loop through each paragraph and append its text to the list
            for p in paragraphs:
                paragraph_list.append(await p.text_content())
        # Close the browser
        await browser.close()
        # Return the list of paragraphs
        return paragraph_list

# Run the async function and print the result
# asyncio.run(get_paragraphs(url))
