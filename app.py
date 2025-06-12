import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

API_KEY = "9b54025852cc28fab3f3e46abba1a2e4"  # You can also use st.secrets["SCRAPER_API_KEY"]

def fetch_reviews(url):
    api_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={url}&render=true"
    response = requests.get(api_url)

    if response.status_code != 200:
        st.error("Failed to load the page from ScraperAPI.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = []

    # Extract all review blocks
    review_blocks = soup.find_all('div', class_='sc-inlrYM')

    for block in review_blocks:
        try:
            user = block.find('p', class_='sc-faswKr')
            review_text = block.find('p', class_='sc-dTOuAs')
            rating = block.find('div', class_='sc-1q7bklc-1')

            reviews.append({
                'User': user.text.strip() if user else 'N/A',
                'Rating': rating.text.strip() if rating else 'N/A',
                'Review': review_text.text.strip() if review_text else 'No review text'
            })
        except Exception as e:
            continue

    return reviews


# Streamlit UI
st.title("🍽️ Zomato Review Scraper (via ScraperAPI)")
url = st.text_input("Enter full Zomato review page URL (must end in `/reviews`)")

if st.button("Scrape Reviews"):
    if url.strip():
        results = fetch_reviews(url.strip())
        if results:
            df = pd.DataFrame(results)
            st.write(df)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "reviews.csv", "text/csv")
        else:
            st.warning("No reviews found or scraping failed.")
    else:
        st.warning("Please enter a valid Zomato URL.")
