import streamlit as st
import requests
from bs4 import BeautifulSoup

SCRAPERAPI_KEY = "9b54025852cc28fab3f3e46abba1a2e4"

def fetch_reviews(zomato_url):
    api_url = f"https://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={zomato_url}&render=false"

    try:
        response = requests.get(api_url, timeout=60)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Failed to fetch the page using ScraperAPI.\n\n{e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    reviews = []

    names = soup.find_all("p", class_="sc-1hez2tp-0 sc-faswKr jihbqh")
    ratings = soup.find_all("div", class_="sc-1q7bklc-1 cILgox")
    types = soup.find_all("div", class_="sc-1q7bklc-9 dYrjiw")
    texts = soup.find_all("p", class_="sc-1hez2tp-0 sc-dTOuAs iuORyl")

    for name, rating, order_type, text in zip(names, ratings, types, texts):
        reviews.append({
            "name": name.get_text(strip=True),
            "rating": rating.get_text(strip=True),
            "order_type": order_type.get_text(strip=True),
            "review": text.get_text(strip=True)
        })

    return reviews

# Streamlit UI
st.title("🍔 Zomato Review Scraper (BeautifulSoup + ScraperAPI)")
zomato_url = st.text_input("Enter Zomato Restaurant Reviews URL:")

if zomato_url:
    with st.spinner("Fetching reviews, please wait..."):
        reviews = fetch_reviews(zomato_url)

    if reviews:
        st.success(f"Found {len(reviews)} reviews!")
        for review in reviews:
            st.markdown(f"**👤 {review['name']}**")
            st.markdown(f"⭐ Rating: {review['rating']} ({review['order_type']})")
            st.markdown(f"📝 {review['review']}")
            st.markdown("---")
    else:
        st.warning("No reviews found or scraping failed.")
