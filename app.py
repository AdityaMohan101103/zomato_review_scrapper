import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_reviews_with_selenium(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)

    # Scroll to load more reviews
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    reviews = []
    review_elements = driver.find_elements(By.CLASS_NAME, "sc-1hez2tp-0")

    for element in review_elements:
        try:
            user = element.find_element(By.CLASS_NAME, "sc-faswKr").text
        except:
            user = "Unknown"
        try:
            text = element.find_element(By.CLASS_NAME, "sc-dTOuAs").text
        except:
            text = "No review"
        try:
            rating = element.find_element(By.CLASS_NAME, "sc-1q7bklc-1").text
        except:
            rating = "No rating"

        reviews.append({"User": user, "Review": text, "Rating": rating})

    driver.quit()
    return reviews

# Streamlit UI
st.title("Zomato Review Scraper (Local with Selenium)")

url = st.text_input("Enter Zomato Restaurant URL:")

if st.button("Scrape Reviews"):
    if url:
        results = scrape_reviews_with_selenium(url)
        if results:
            df = pd.DataFrame(results)
            st.write(df)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "zomato_reviews.csv", "text/csv")
        else:
            st.warning("No reviews found or scraping failed.")
    else:
        st.warning("Please enter a valid Zomato URL.")
