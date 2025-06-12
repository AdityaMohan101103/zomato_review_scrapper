import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

# Extract embedded review data from Zomato page
def scrape_reviews(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error("Failed to retrieve the page. Please check the URL.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", text=re.compile("zomatoReduxData"))

    if not script_tag:
        st.warning("Could not find embedded data in the page.")
        return []

    try:
        json_text = re.search(r"zomatoReduxData\s*=\s*({.*});", script_tag.string).group(1)
        data = json.loads(json_text)
    except Exception as e:
        st.error("Failed to parse embedded JSON data.")
        return []

    # Traverse JSON to get reviews
    try:
        restaurant_id = next(iter(data["pages"]["restaurant"]["sections"].values()))["resId"]
        reviews = data["entities"]["REVIEWS"]
    except:
        st.warning("No reviews found in data.")
        return []

    review_list = []
    for review_id, review_data in reviews.items():
        user = review_data.get("userName", "Unknown")
        rating = review_data.get("rating", "No rating")
        text = review_data.get("reviewText", "No review")
        review_list.append({"User": user, "Rating": rating, "Review": text})

    return review_list

# Streamlit UI
st.title("Zomato Review Scraper (Requests + BeautifulSoup)")

url = st.text_input("Enter Zomato Restaurant URL:")

if st.button("Scrape Reviews"):
    if url:
        reviews = scrape_reviews(url)
        if reviews:
            df = pd.DataFrame(reviews)
            st.write(df)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "zomato_reviews.csv", "text/csv")
        else:
            st.info("No reviews found or failed to scrape.")
    else:
        st.warning("Please enter a valid Zomato URL.")
