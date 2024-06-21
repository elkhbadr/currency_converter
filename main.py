#!/usr/bin/env python3

import os
import requests
from currencies import currencies
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")
base_url = "https://v6.exchangerate-api.com/v6"

def verify_currencies_input(from_curr, to_curr):
    """
    This function checks that the user has not made a mistake in the currencies
    """
    if from_curr in currencies and to_curr in currencies:
        # Ask for confirmation from the user
        confirmed_from = input(f"Do you really want to convert from {currencies[from_curr]} ({from_curr}) ? (yes/no) ").lower()
        if confirmed_from != "yes":
            return False
        
        confirmed_to = input(f"Do you really want to convert to {currencies[to_curr]} ({to_curr}) ? (yes/no) ").lower()
        if confirmed_to != "yes":
            return False
        
        return True
    else:
        return False

def get_exchange_rate(from_curr, to_curr):
    """
    This function makes a request to the API to get exchange rates for both currencies
    """
    url = f"{base_url}/{api_key}/pair/{from_curr}/{to_curr}"
    print(url)
    
    try:
        response = requests.get(url)
        data = response.json()

        # Check if request was successful
        if response.status_code != 200:
            print(f"Error during request: {data['error']}")
            return None

        # Retrieve exchange rate
        exchange_rate = data["conversion_rate"]
        return exchange_rate

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def calculate_conversion(amount, exchange_rate):
    """
    This function calculates the converted amount using the given exchange rate.
    """
    if exchange_rate is None:
        return None
    
    converted_amount = amount * exchange_rate
    return converted_amount

if __name__ == "__main__":
    currency_from = input("Enter the currency code you want to convert from: ").upper()
    currency_to = input("Enter the currency code you want to convert to: ").upper()
    amount = float(input("Enter the amount to convert: "))

    if verify_currencies_input(currency_from, currency_to):
        exchange_rate = get_exchange_rate(currency_from, currency_to)
        if exchange_rate is not None:
            converted_amount = calculate_conversion(amount, exchange_rate)
            if converted_amount is not None:
                print(f"{amount} {currency_from} is equivalent to {converted_amount:.2f} {currency_to}")
            else:
                print("Failed to calculate conversion.")
        else:
            print("Failed to retrieve exchange rate.")
    else:
        print("Conversion canceled.")
