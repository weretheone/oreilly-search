import requests
import re
import pandas as pd
import numpy as np
from datetime import datetime

# This is the search term you want search on the platform 
search_term = 'python'

# Make an API call for the search and store the response.
url = f'https://learning.oreilly.com/api/v2/search/?query={search_term}&extended_publisher_data=true&source=user&formats=live%20online%20training&limit=200'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Store API' JSON response in a dictonary
response_dict = r.json()

# Store the results part of the response
search_results = response_dict['results']

# Define lists for the things you want to store
titles, web_urls, starts, ends, authors = [], [], [], [], []

for entry in search_results:
    # Collect the title
    title = entry['title']
    titles.append(title)
    # Collect the event to get the time
    event = entry['events']
    # Grab only the first part of the long event string
    event_part = event[1:92]
    # Split it based on the quote sign
    splitted_line = re.split('"', event_part)
    # Grab the start time and add it to our list
    start = splitted_line[3]
    starts.append(start)
    # Grab the end time and add it to our list
    end = splitted_line[7]
    ends.append(end)
    # Collect the url and append it to the base url then add to a list
    url = entry['web_url']
    web_url = f' <a href="https://learning.oreilly.com{url}">{title}</a> '
    #web_url = f'https://learning.oreilly.com{url}'
    web_urls.append(web_url)
    # Grab the author and add it to the list
    author = entry['authors']
    authors.append(author)

# Add the lists to a dataframe
df = pd.DataFrame(list(zip(starts, ends, titles, web_urls, authors)),
                columns = ['Start', 'End', 'Title', 'URL', 'Presenter'])
# Sort the values on 'Start time'
df.sort_values(by = ['Start'], inplace=True, ignore_index=True)
# Modify datatype for start and end time
df[['Start','End']] = df[['Start','End']].astype('datetime64')
# Add my timezone difference +2 (CET) 
df['Start'] = df['Start'] + np.timedelta64(2, 'h')
df['End'] = df['End'] + np.timedelta64(2, 'h')
# Calculate duration
duration = df['End'] - df['Start']
# Grab the Hours and minutes part
hours = duration.dt.components['hours']
minutes = duration.dt.components['minutes']
# Convert them to string
hours = hours.astype(str)
minutes = minutes.astype(str)
# Format and add the created column
duration= hours + 'h ' + minutes + 'm'
df.insert(loc = 1, column = 'Duration', value = duration)


# Slice what you want as output and save as HTML
df_final=  df[['Start', 'Duration', 'URL', 'Presenter']].copy()
filename = f'oreilly_{search_term}_online_educations.html'
df_final.to_html(filename, render_links=True, escape=False,)

# Append the creation date, time to the HTML
current_date = datetime.now().date()
with open(filename, 'a') as file: 
    file.write(f"The list generated at {current_date}") 
