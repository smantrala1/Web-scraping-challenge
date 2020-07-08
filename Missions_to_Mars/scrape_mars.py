from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time 

def scrape():
     

    # --- Visit Mars News site ---
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    for x in range(5):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('li', class_='slide')
        #print(articles)
    
    
    
    for a in articles:
        news_title = a.h3.text
    news_p = articles[0].find('div', class_='article_teaser_body').text
    print(news_title)
    print(news_p)


    
    # --- Visit JPL site for featured Mars image ---
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    attempts = 0
    for x in range(3):
        attempts += 1
        try:
            # scraper for JPL
            url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
            browser.visit(url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            browser.links.find_by_partial_text('FULL IMAGE').click()
            time.sleep(1)
            browser.links.find_by_partial_text('more info').click()
            time.sleep(1)
            browser.find_by_xpath('//*[@id="page"]/section[1]/div/article/figure/a/img').click()
            time.sleep(1)
            image_url = browser.url
            
            break
        except Exception as e:
            print(f"Error scraping JPL images: {e}")
        if attempts == 3:
            image_url = ""
    

    # --- Use Pandas to scrape Mars Space Facts ---
    tables = pd.read_html('https://space-facts.com/mars/')

    # Take second table for Mars facts
    df = tables[0]

    # Rename columns and set index
    df.columns=['description', 'value']
    
    # Convert table to html
    mars_facts_table = df.to_html(classes='data table', index=False, header=False, border=0)
    #browser.visit(image_url)



    # --- Visit USGS Astrogeology Site ---
    mars_hemispheres='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres)
    
    
    html_hemispheres = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    
    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    
    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    
    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
    
    # Display hemisphere_image_urls
    hemisphere_image_urls
    

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": image_url,
        "mars_facts": mars_facts_table,
        "hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data