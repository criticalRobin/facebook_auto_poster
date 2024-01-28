import os
import json
import random
from dotenv import load_dotenv
from logs import logger
from time import sleep
from scraping_manager.automate import WebScraping
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Read env vars 
load_dotenv ()
CHROME_FOLDER = os.getenv ("CHROME_FOLDER")
WAIT_MIN = int(os.getenv ("WAIT_MIN"))

class Scraper (WebScraping):
    
    def __init__ (self):
        """ read data from json file and start scraper using chrome folder """
        
        # Files paths
        current_folder = os.path.dirname(__file__)
        self.data_path = os.path.join (current_folder, "data.json")

        # Read json data
        with open (self.data_path, encoding="UTF-8") as file:
            self.json_data = json.loads (file.read())

        # Start scraper
        super().__init__(chrome_folder=CHROME_FOLDER, start_killing=True)
        
    def post_in_groups (self):
        """ Publish each post in each group fromd ata file """

        # Css selectors
        selectors = {
            "display_input": ".x6s0dn4.x78zum5.x1l90r2v.x1pi30zi.x1swvt13.xz9dl7a > span.x1emribx + div.x1i10hfl",
            "input": 'div.notranslate._5rpu[role="textbox"]',
            "display_themes": 'div[aria-label="Show Background Options"]',
            "theme": 'div.x1qjc9v5.x78zum5.x1q0g3np.xozqiw3.xcud41i.x139jcc6.x1n2onr6.xl56j7k > div:nth-child(index) > div[aria-pressed="false"]',
            "show_image_input": '[aria-label="Photo/video"]',
            "add_image": 'input[type="file"][accept^="image/*"]',
            "submit": '[aria-label="Post"][role="button"], [aria-label="Publicar"][role="button"]',
        }

        posts_done = []
        for group in self.json_data["groups"]:
            self.set_page(group)
            wait = WebDriverWait(self.driver, 30)
            
            # Wait for and open text input
            try:
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectors["display_input"]))).click()
                post = random.choice(self.json_data["posts"])                
                post_text = post["text"]
                post_image = post.get("image", "")

                # Find the input element and send post text
                input_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectors["input"])))
                input_element.send_keys(post_text)
                
                # Upload image if available
                if post_image:
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectors["show_image_input"]))).click()
                    image_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectors["add_image"])))
                    image_input.send_keys(post_image)
                
                # Submit post
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors["submit"]))).click()
                sleep(WAIT_MIN * 60)
                posts_done.append([group, post])
                logger.info(f'Post done: "{post}" ({group})')

            except Exception as e:
                logger.error(f'Error in group {group}: {e}')
                continue
                
    def save_groups (self, keyword):
        """ Sedarch already signed groups and save them in data file """
        
        # Set groups page
        logger.info ("Searching groups...")
        search_page = f"https://www.facebook.com/groups/search/groups/?q={keyword}"
        self.set_page(search_page)
        sleep (3)
        self.refresh_selenium()
        
        links_num = 0
        tries_count = 0
        
        selectors = {
            "group_link": '.x1yztbdb div[role="article"] a[aria-label="Visit"]',
        }
        
        # Scroll for show already logged groups
        while True:
            self.go_bottom()
            new_links_num = len(self.get_elems (selectors["group_link"]))
            if new_links_num == links_num:
                tries_count += 1
            else: 
                links_num = new_links_num
                self.refresh_selenium()
                
            if tries_count == 3:
                break
            
        # Get all link of the groups
        links = self.get_attribs (selectors["group_link"], "href")
        logger.info (f"{len(links)} groups found and saved")
        
        # Save links in jdon file
        if links:
            self.json_data["groups"] = links
            with open (self.data_path, "w", encoding="UTF-8") as file:
                file.write (json.dumps(self.json_data))
                
            
        
         
