import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def scrape_reviews_with_selenium(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service("chromedriver")  # Path to ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    time.sleep(5)  # Give time for reviews to load

    usernames = [el.text for el in driver.find_elements(By.CLASS_NAME, "sc-faswKr")]
    ratings = [el.text for el in driver.find_elements(By.CLASS_NAME, "sc-1q7bklc-1")]
    reviews = [el.text for el in driver.find_elements(By.CLASS_NAME, "sc-dTOuAs")]

    driver.quit()

    if not usernames or not reviews:
        return []

    data = []
    for i in range(min(len(usernames), len(reviews))):
        data.append({
            "User": usernames[i],
            "Rating": ratings[i] if i < len(ratings) else "No Rating",
            "Review": reviews[i]
        })
    return data

# Streamlit App
st.title("🍔 Zomato Review Scraper")

url = st.text_input("Enter Zomato Restaurant Reviews URL:")

if st.button("Scrape Reviews"):
    if url:
        with st.spinner("Fetching reviews, please wait..."):
            results = scrape_reviews_with_selenium(url)
        if results:
            df = pd.DataFrame(results)
            st.write(df)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "zomato_reviews.csv", "text/csv")
        else:
            st.error("No reviews found or scraping failed.")
    else:
        st.warning("Please enter a valid Zomato URL.")
