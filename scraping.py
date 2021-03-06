
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#10.5.3 Integrate Mongo
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    #why =true?
#does the below go here?10.5.3 says this line pulls this data. it is possible. 
#does it need to be indented?
    news_title, news_paragraph = mars_news(browser)
#10.5.3 browser ready to work, create the data dictionary

# Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemisphere": hemisphere_img(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

#10.5.2 add try prior to scrape. so why below? doesnt matter
#try:
    #slide_elem = news_soup.select_one('div.list_text')
    # Use the parent element to find the first 'a' tag and save it as 'news_title'
    #news_title = slide_elem.find('div', class_='content_title').get_text()
    # Use the parent element to find the paragraph text
    #news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    #except AttributeError:
    #return None, None

def mars_news(browser):
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    #10.3.3 in JNB added news_title & news_p as python return statement
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

     # TODO:
    # return JSON data
    #10.5.2 Update the code. here it says to update feature by defining function.
    #where does this tie in? so lets place below as missing.

#def featured_image(browser):
    #remove print statements and return them.
    #return img_url
    #try:
    # find the relative image url
    #img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    #except AttributeError:
    #return None

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
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
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemisphere_img(browser):

    #10.5.3 Integrate Mongo. i put in the front. seemed to make sense.
    #19.5.3 Now asking to close.
    # Stop webdriver and return data
    
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = [] 

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #first get a list
    links = browser.find_by_css('a.product-item img')

    #next loop through links, click link 
    for i in range(len(links)):
        hemisphere = {}
        
        #first_click = browser.links.find_by_partial_text('Cerberus').click()
        browser.find_by_css('a.product-item img')[i].click()

        #sample image anchor tag
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url']=sample_elem['href']
        
        #get title
        hemisphere['title']=browser.find_by_css('h2.title').text
        
        #append hemiphere object to list
        hemisphere_image_urls.append(hemisphere)

        #links
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls
 


   
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

