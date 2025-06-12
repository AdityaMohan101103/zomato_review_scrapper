import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

SCRAPER_API_KEY = "YOUR_API_KEY"  # Replace with your ScraperAPI key

def fetch_rendered_html(url):
    api_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={url}&render=true"
    response = requests.get(api_url)
    return response.text if response.status_code == 200 else None

def scrape_reviews_bs(url):
    html = fetch_rendered_html(url)
    if not html:
        st.error("Failed to fetch rendered HTML.")
        return []

    soup = BeautifulSoup(html, "html.parser")
    reviews = []

    review_blocks = soup.find_all("div", class_="sc-inlrYM ikYBPh")
    for block in review_blocks:
        name_tag = block.find("p", class_="sc-faswKr")
        review_tag = block.find("p", class_="sc-dTOuAs")
        rating_tag = block.find("div", class_="sc-1q7bklc-1")

        name = name_tag.text if name_tag else "Unknown"
        review = review_tag.text if review_tag else "No Review"
        rating = rating_tag.text if rating_tag else "No Rating"

        reviews.append({
            "User": name,
            "Review": review,
            "Rating": rating
        })

    return reviews

# Streamlit UI
st.title("Zomato Review Scraper (BeautifulSoup + ScraperAPI)")

url = st.text_input("Enter Zomato Review Page URL")

if st.button("Scrape Reviews"):
    if url:
        results = scrape_reviews_bs(url)
        if results:
            df = pd.DataFrame(results)
            st.write(df)
            st.download_button("Download CSV", df.to_csv(index=False), "zomato_reviews.csv", "text/csv")
        else:
            st.warning("No reviews found or failed to scrape.")
    else:
        st.warning("Please enter a valid Zomato URL.")
