# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Setting the executable path which initializes a browser
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # returning the output of our mars_news function into the news_title and news_paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(), # Returns the date this code was ran
        "image_dictionary": mars_images(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Scrape Mars News
    
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_images(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    # 2. Create a dictionary to hold the images and titles.
    image_list_of_dictionary = []

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
            
            # Creating temp dictionary
            image_dictionary = {}
            
            # Finding image title
            image_title = temp_html_soup.find('h2').get_text().strip()
            print(image_title)
            
            # Finding the image src and creating a link
            image_src = temp_html_soup.find('img', class_='wide-image').get('src')
            image_url = (f'{url}{image_src}')
            
            image_dictionary['img_url'] = image_url
            image_dictionary['title'] = image_title
            
            # Appending the fake temp into the list of dictionaries
            image_list_of_dictionary.append(image_dictionary)
        
        return image_list_of_dictionary

    except BaseException:
        return "None"
        
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())