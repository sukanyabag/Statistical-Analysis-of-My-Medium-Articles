from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
#import numpy as np
import pandas as pd

USER = ' '
PASS = ' '

def login_to_medium(driver, email, password):
    
    #user sign in
    driver.get('https://medium.com/m/signin')
    
    #sign-in
    driver.find_element_by_xpath(".//button[contains(., 'Sign in')]").click()
    
    #sign-in with Google
    driver.find_element_by_xpath(".//button[contains(., 'Sign in with Google')]").click()
    
    #select email for identification
    email_field = driver.find_element_by_id("identifierID")
    
    #writes email
    email_field.send_keys(email)
    
    #selecitng next button for password field
    driver.find_element_by_id("identifierNext").click()
    
    #sleep for a sec or two
    time.sleep(1)
    
    #locate password field
    password_field = driver.find_element_by_name("password")
    
    #writes password
    password_field.send_keys("password")
    
    #selecting next button
    driver.find_element_by_id("passwordNext").click()
    
    #wait for a moment
    time.sleep(3)
    
    #navigating to the stats page
    driver.get('https://medium.com/me/stats')
    
    
    #scrolling to bottom of the page to view all pubs
    
    def scroll_down(driver):
        SCROLL_PAUSE_TIME = 0.5
        
        #scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            #scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #page-loading
            time.sleep(SCROLL_PAUSE_TIME)
            #compute new scroll height and compare with last one
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            
            last_height = new_height
            
        
        
    def extract_info(driver):
        
        #table html from medium stats 
        table_html = driver.find_element_by_class_name('js-statsTableBody')
        
        #raw html from table element
        raw_html = table_html.getattribute('innerHTML')
        
        #quit driver
        driver.quit()
        
        #html cleaning
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        #story titles
        story_titles = [item.text for i, item in enumerate(soup.select('h2'))]
        
        #read times of followers/readers
        read_times = [item.get('title') for i,item in enumerate(soup.findAll('span', {'class':'readingTime'}))]
        
        #publication names
        publications = []
        
        h2tags = soup.findAll('h2')
        
        for h2tag in h2tags:
            page = [str(h2tag)]
            elem = h2tag.next_sibling
            
            while elem and elem.name != 'h2':
                if elem.text.split('View story')[0]=='':
                    publications.append(None)
                    
                else:
                    '''
                    what the 1 liner is doing -
                    elem.text = "In Python in Plain English View story Details"
                    x = elem.text.split('View story')[0][3::]
                    print(x)

                    #txt.split('View story')-> ['In Python in Plain English ', ' Details']
                    #txt.split('View story')[0]-> In Python in Plain English 
                    #txt.split('View story')[0][3::]-> Python in Plain English-> publication name
                    '''
                    publications.append(elem.text.split('View story')[0][3::])
                elem = elem.next_sibling
            
            
        #numerical data 
        num_vals = [item.text for i, item in enumerate(soup.findAll('span',{'class':'sortableTable-value'})) 
                    if (len(item.text) < 13 or '.' in item.text)]
        
        #num_vals = [437,97,22,19]
        #views = num_vals[::4] -> 437 views
        views = num_vals[::4]
        
        #num_vals = [437,97,22,19]
        #reads = num_vals[1::4] -> 97 reads
        reads = num_vals[1::4]
        
        #num_vals = [437,97,22,19]
        #read_ratio = num_vals[2::4] -> 22 read-ratio
        read_ratio = num_vals[2::4]
        
        #num_vals = [437,97,22,19]
        #fans = num_vals[3::4] -> 19 fans
        fans = num_vals[3::4]
        
        #creating dataframe to store the data
        df = pd.DataFrame(data = {'Title': story_titles, 'Read Time': read_times, 'Publications': publications,
                                  'Views': views, 'Reads': reads, 'Read Ratio': read_ratio, 'Fans': fans})
        
        #reordering the columns
        df = df[['Title', 'Publication', 'Read Time', 'Views', 'Reads', 'Read Ratio', 'Fans']]
        
        #turn numerical features into floats
        df = df.apply(pd.to_numeric, errors = 'ignore')
        
        #returns only 11 and not 11 mins
        df['Read Time'] = df['Read Time'].apply(lambda x: int(x.split()[0]))
        
        
        return df
    
    def show_info(df):
        for index, row in df.iterrows():
            if index == 0:
                print("**************************************")
            
            print('Title:', row['Title'])
            print('Read Time:', row['Read Time'])
            print('Publication:', row['Publication'])
            print('Views:', row['Views'])
            print('Reads:', row['Reads'])
            print('Read Ratio:', row['Read Ratio'])
            print('Fans:', row['Fans'])
            
            print("Sukanya's Writer Statistics @ Medium")
            
            time.sleep(.3)
            
            
    if __name__ == "__main__":
        
        driver = webdriver.Chrome(ChromeDriverManager().install())
        
        #logs in
        login_to_medium(driver, USER, PASS)
        
        #scroll
        scroll_down(driver)
        
        #export data as csv to the local machine
        df = extract_info(driver)
        show_info(df)
        df.to_csv('Sukanya_Writer_Stats.csv', index= False)
        print("Your writer stats at Medium is created and saved in Sukanya_Writer_Stats.csv!")
        
        
            
            
            
            
            
        
        
        
        
        
        
        
        
        
    
    