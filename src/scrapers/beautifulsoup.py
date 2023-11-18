# Import the requests and BeautifulSoup libraries
import requests
from bs4 import BeautifulSoup

# Specify the URL of the website to scrape
url = "https://www.alarabiya.net/aswaq/special-stories/2023/11/16/%D9%85%D8%B4%D9%83%D9%84%D8%A9-%D8%A7%D9%84%D8%AA%D8%B1%D9%8A%D9%84%D9%8A%D9%88%D9%86-%D8%AF%D9%88%D9%84%D8%A7%D8%B1-%D9%83%D9%8A%D9%81-%D8%AA%D9%88%D8%A7%D8%AC%D9%87%D9%87%D8%A7-%D8%A7%D9%84%D8%A8%D9%86%D9%88%D9%83-%D8%A7%D9%84%D9%85%D8%B1%D9%83%D8%B2%D9%8A%D8%A9-%D8%A7%D9%84%D8%B1%D8%A6%D9%8A%D8%B3%D9%8A%D8%A9%D8%9F"

# Make a GET request to the website and store the response
response = requests.get(url)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    # Parse the response content as HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the <div> and <main> tags in the HTML document
    divs_and_mains = soup.find_all(["div", "main"])

    # Create an empty list to store the paragraph texts
    paragraph_list = []

    # Loop through each <div> or <main> tag
    for tag in divs_and_mains:
        # Find all the <p> tags inside the tag
        paragraphs = tag.find_all("p")

        # Loop through each paragraph and append its text to the list
        for p in paragraphs:
            paragraph_list.append(p.text)

    # Print the list of paragraphs
    print(paragraph_list)
else:
    # Print an error message if the response status code is not 200
    print(f"Error: Unable to access the website. Status code: {response.status_code}")
