
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    newstitle,newsp = news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "title": newstitle,
        "paragraph": newsp,
        "feature_image": feature_image(browser),
        "facts": mars_facts(),
        "hemisphere": hemisphere_image(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def news (browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    news_p
    return news_title, news_p

def feature_image (browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_soup

    # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url_rel

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# Scrape Mars News
def hemisphere_image(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_soup

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    links = browser.find_by_tag('h3')
    print(len(links))

    for link in links:
        print(link.text)


    for i in range(len(links)):
        if browser.find_by_tag('h3')[i].text != "":
            hemisphere = {}
            browser.find_by_tag('h3')[i].click()
            sample_element = browser.links.find_by_text('Sample').first
            hemisphere['url'] = sample_element['href']
            hemisphere['title'] = browser.find_by_tag('h2.title').text
            hemisphere_image_urls.append(hemisphere)
            browser.back()

    #print(hemisphere_image_urls)
    hemisphere_image_urls

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

# ## Mars Facts
def mars_facts():

    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
      return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())

