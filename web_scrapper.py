import requests
from bs4 import BeautifulSoup
import lxml
import csv
import time
import random

def web_scrapper2(web_url, f_name):
    # greetings
    print("Thank you for sharing the URL and file name!\n⏳\nReading the content...")

    # Random delay to avoid being blocked
    num = random.randint(3, 7)
    time.sleep(num)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/133.0.0.0 Safari/537.36'
    }

    response = requests.get(web_url, headers=headers)

    if response.status_code == 200:
        print("Connected to the website successfully!")
        html_content = response.text

        # creating soup
        soup = BeautifulSoup(html_content, 'lxml')

        # main containers for hotels
        hotel_divs = soup.find_all('div', role="listitem")

        with open(f'{f_name}.csv', 'w', encoding='utf-8', newline='') as file_csv:
            writer = csv.writer(file_csv)

            # adding header
            writer.writerow(['hotel_name', 'location', 'price', 'rating', 'reviews', 'link'])

            for hotel in hotel_divs:
                # Hotel name
                hotel_name_tag = hotel.find("div", {"data-testid": "title"})
                hotel_name = hotel_name_tag.text.strip() if hotel_name_tag else "NA"

                # Location
                location_tag = hotel.find("span", {"data-testid": "address"})
                location = location_tag.text.strip() if location_tag else "NA"

                # Price
                price_tag = hotel.find("span", {"data-testid": "price-and-discounted-price"})
                price = price_tag.text.strip().replace("₹", "").replace(",", "") if price_tag else "NA"

                # Rating (numeric like 8.2)
                rating_tag = hotel.find("div", {"data-testid": "review-score"})
                rating = rating_tag.text.strip() if rating_tag else "NA"

                # Number of reviews
                review = "NA"
                if rating_tag and rating_tag.find_next("div"):
                    review = rating_tag.find_next("div").text.strip()

                # Hotel link
                link_tag = hotel.find("a", {"data-testid": "title-link"}, href=True)
                link = "https://www.booking.com" + link_tag["href"] if link_tag else "NA"

                # saving the file into csv
                writer.writerow([hotel_name, location, price, rating, review, link])

        print("Web scraping done! Data saved in", f"{f_name}.csv")

    else:
        print(f"Connection Failed! Status code: {response.status_code}")


# If using this script directly, run this
if __name__ == '__main__':
    url = input("Please enter Booking.com search URL: ")
    fn = input("Please enter file name (without extension): ")

    # calling the function
    web_scrapper2(url, fn)
    
