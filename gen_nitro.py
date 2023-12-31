import requests
import datetime
import concurrent.futures
import json

headers = {
    'authority': 'api.discord.gx.games',
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.opera.com',
    'referer': 'https://www.opera.com/',
    'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0',
}

json_data = {
    'partnerUserId': 'bc385c68-be5f-43c2-9713-cb2051fef65b',
}

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Prompt the user for the number of tokens to generate
num_tokens = int(input("Enter the number of tokens to generate: "))

# Create a timestamp for the file name
timestamp = datetime.datetime.now().strftime("%d %m %Y_%H %M %S")

# Open a file with the current timestamp as the name
file_name = f"{num_tokens}_generated_urls_{timestamp}.txt"
with open(file_name, 'w') as file:
    # Function to process a single token
    def process_token(counter):
        response = requests.post('https://api.discord.gx.games/v1/direct-fulfillment', headers=headers, json=json_data)
        if response.status_code == 200:
            response_data = response.json()
            token = response_data.get('token', '')
            url = f'https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n'
            file.write(url)
            print(f"Token Valid No {counter}\n")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    # Use threading to process tokens concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=config['num_threads']) as executor:
        # Pass a counter to the process_token function
        executor.map(process_token, range(1, num_tokens + 1))

print(f"Generated {num_tokens} URLs and saved them to {file_name}")
