import streamlit as st
import requests
from bs4 import BeautifulSoup

SCRAPERAPI_KEY = "9b54025852cc28fab3f3e46abba1a2e4"

st.set_page_config(page_title="Zomato Review Scraper", layout="centered")
st.title("🍔 Zomato Review Scraper (BeautifulSoup + ScraperAPI)")

url = st.text_input("Enter Zomato Restaurant Reviews URL:")

def get_soup_with_scraperapi(zomato_url):
    api_url = f"http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={zomato_url}&render=true"
    try:
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        st.error(f"Request failed: {e}")
    return None

def extract_reviews(soup):
    reviews = []

    names = soup.select("p[class*='sc-faswKr']")
    ratings = soup.select("div[class*='sc-1q7bklc-1']")
    types = soup.select("div[class*='sc-1q7bklc-9']")
    comments = soup.select("p[class*='sc-dTOuAs']")

    for i in range(len(comments)):
        review = {
            "Reviewer": names[i].text.strip() if i < len(names) else "",
            "Rating": ratings[i].text.strip() if i < len(ratings) else "",
            "Type": types[i].text.strip() if i < len(types) else "",
            "Comment": comments[i].text.strip() if i < len(comments) else "",
        }
        reviews.append(review)
    return reviews

if url:
    if "zomato.com" not in url or "/reviews" not in url:
        st.warning("Please enter a valid Zomato reviews page URL (must include '/reviews').")
    else:
        st.info("Fetching reviews, please wait...")
        soup = get_soup_with_scraperapi(url)
        if soup:
            results = extract_reviews(soup)
            if results:
                st.success(f"✅ Found {len(results)} reviews!")
                for r in results:
                    st.markdown(f"**{r['Reviewer']}** ({r['Type']}, ⭐ {r['Rating']})")
                    st.markdown(f"📃 {r['Comment']}")
                    st.markdown("---")
            else:
                st.warning("No reviews found or scraping failed.")
        else:
            st.error("Failed to fetch the page using ScraperAPI.")
