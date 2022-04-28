# Import Splinter and BeautifulSoup
from unittest.mock import Base
from matplotlib import image
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setting the executable path which initializes a browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site - assigning the url we want to scrape from
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page - look below for additional comments
browser.is_element_present_by_css('div.list_text', wait_time=1)


# The third line of code seaches for elements with a specific combination of tag (div) and attribute (list_text):
# 
#     - This looks like < div class="list_text" >
#     
# The line also adds a delay before searching for the other components
#     
#     - This is usefull especially for pages that take a while to load

# In[4]:


# Retrieves the html data from the browser
html = browser.html

# Soup parses the html data/ gives it structure
news_soup = soup(html, 'html.parser')

# Selecting all div with a element of 'list_test' - parent element which we'll search through to find other contained elements
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# looking throught the parent element - we are finding all nested divs with a class 'content_title' - assign to object
news_title = slide_elem.find('div', class_='content_title').get_text().strip()


# In[6]:


news_title


# In[7]:


# Use the parent element to find the FIRST - which is the first articles paragraph - paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text().strip()
news_p


# ### Featured Images

# In[8]:


# Indicating the URL and visiting
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Finds and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


img_soup


# In[12]:


# Find the relative image URL - that is what getting the src does, specifies the location in the url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[14]:


# Goal is to extract the first table from a website that have the <table/> tag - and convert it into a pandas DB

# the pd function 'read_html' specifically searches and returns a list of tables found in the html - we index for the 1st one
df = pd.read_html('https://galaxyfacts-mars.com')[0]

# Creating DB columns
df.columns=['description', 'Mars', 'Earth']

# Setting index to descrtiption
df.set_index('description', inplace=True)
df


# In[15]:


# Turning the table back into html using pandas 'to_html' function
df.to_html()


# In[16]:


# Ends the session
browser.quit()


# # Challenge start

# In[32]:


# Setting the executable path which initializes a browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[37]:

def mars_images(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    # 2. Create a dictionary to hold the images and titles.
    image_dictionary = {}

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # Parse the current browsers html using bewutiful soup
    html = browser.html
    html_soup = soup(html, 'html.parser')

    try:
        # Container that contains all the link boxes and their divs w/ links we want to access
        full_image_container = html_soup.find('div', class_='collapsible results')

        # Creating a list that contains all the boxes htmls that have access to the images href
        link_boxes = full_image_container.find_all('div', class_='item')

        # We'll create a for loop to go through each of the href and click full image 
        for x in range(len(link_boxes)):
            # Going through each tag, and visiting their links
            image_href = link_boxes[x].find('a', class_='itemLink product-item').get('href')
            full_link = f'{url}{image_href}'
            browser.visit(full_link)
            
            # Parsing each links html
            temp_html = browser.html
            temp_html_soup = soup(temp_html, 'html.parser')
            
            # Finding image title
            image_title = temp_html_soup.find('h2').get_text().strip()
            print(image_title)
            
            # Finding the image src and creating a link
            image_src = temp_html_soup.find('img', class_='wide-image').get('src')
            print(f'{url}{image_src}')
            
            image_dictionary[image_title] = image_src
        
        return image_dictionary

    except BaseException:
        return None

    


# In[38]:


# 4. Print the list that holds the dictionary of each image url and title.
image_dictionary


# In[39]:


# 5. Quit the browser
browser.quit()


# In[ ]:




