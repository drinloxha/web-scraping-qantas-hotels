import requests
from bs4 import BeautifulSoup
import csv

# Replace the URL with the actual URL of the website
url = "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-02-01&checkOut=2024-02-02&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity"

# Make a request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract information
rates = []

# Iterate over each offer card
for offer_card in soup.find_all('div', class_='css-ohihuc-Box-Flex'):
    room_name = offer_card.find('h3', class_='css-1negoe1-Heading-Heading-Text e13es6xl3').text.strip()
    rate_name = offer_card.find('span', class_='css-u2xec8-Text e1j4w3aq0').text.strip()
    guests = offer_card.find('span',
                             class_='css-u2xec8-Text e1j4w3aq0').text.strip()  # Assuming this is the number of guests
    cancellation_policy = offer_card.find('button', class_='css-12hhnd3 e1ucyleq0').text.strip()
    price = offer_card.find('span', class_='css-1bjudru e1c6pi2o1').text.strip()
    currency = offer_card.find('span', class_='css-17uh48g-Text e1j4w3aq0').text.strip()

    # Check if it's a Top Deal
    top_deal = bool(offer_card.find('span', class_='css-1jr3e3z-Text-BadgeText e34cw120'))

    # Create a list for each offer card
    rate_info = [room_name, rate_name, guests, cancellation_policy, price, top_deal, currency]

    rates.append(rate_info)

# Write the information to a CSV file
csv_file_path = 'hotel_rates.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header
    csv_writer.writerow(
        ['Room_name', 'Rate_name', 'Number_of_Guests', 'Cancellation_Policy', 'Price', 'Is_Top_Deal', 'Currency'])

    # Write the data
    csv_writer.writerows(rates)

print(f"Data has been written to {csv_file_path}")
