import requests
import pandas as pd

# Define the area parameter
area_param = '32'
# start_row_id = 7776900
# Set up API request parameters
api_key = 'TEST123'
callback = 'getcontacts'
url = 'https://cmd.smsairworks.com/api/v1/'
headers = {
    'Api-Key': api_key,
    'Content-Type': 'application/x-www-form-urlencoded',
    # Assuming 'PHPSESSID' is retrieved elsewhere (e.g., login)
    'Cookie': 'PHPSESSID=your_phpsessid'  # Replace with your actual PHPSESSID value
}
data = {
    'callback': callback,
    'county_id': area_param,  # Replace with the actual area parameter
    'limit': 130000,
    # 'start_row_id': start_row_id
}

try:
    # Send the API request
    response = requests.get(url, headers=headers, data=data)
    response.raise_for_status()  # Raise exception for non-2xx status codes

    # Extract phone numbers from the response
    json_data = response.json()
    contacts = json_data.get('contacts', [])
    phone_numbers = [contact['phone'] for contact in contacts if contact.get('phone')]
    
    # Write phone numbers to CSV
    df = pd.DataFrame({'phone_number': phone_numbers})
    df.to_csv('nakuru.csv', index=False)
    
    print('Phone numbers successfully written to homabay.csv')

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
