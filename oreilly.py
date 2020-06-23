import requests
import re

# Make an API call and store the response.
url = 'https://learning.oreilly.com/api/v2/search/?query=python&extended_publisher_data=true&source=user&formats=live%20online%20training&limit=100'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Store API' JSON response in a dictopnary
response_dict = r.json()

# Store the results part of the response
search_results = response_dict['results']

# Define what to store
titles, web_urls, starts = [], [], []

for entry in search_results:
    # Collect the title
    title = entry['title']
    titles.append(title)
    # Collect the event to get the time
    event = entry['events']
    # Grab only the first part of the long string
    event_part = event[1:92]
    # Split it based on the quote sign
    splitted_line = re.split('"', event_part)
    # Grab the start time and add it to our list
    start = splitted_line[3]
    starts.append(start)
    # Collect the url and create a clickable link including the title and the 
    # start time (UTC) of the event
    url = entry['web_url']
    web_url = f"<a href='https://learning.oreilly.com{url}'>{start} - {title}</a><br>"
    web_urls.append(web_url)
    

#Create an HTML file for testing
filename = 'python_online.html'
with open(filename, 'w') as f:
    print(web_urls, file=f)