# ----------------------------------------------------------------------------------------------------
# Authur: creativeJoe007
# Github: https://github.com/creativeJoe007/instagram-leads-scraper
# Website: https://creativejoe007.com
#----------------------------------------------------------------------------------------------------
# An instagram bot that allows anyone search for businesses/influencers using a keyword
# We extract the business name, profile picture, email (if any), mobile number (if any), followers, 
# followings, total posts, bio, profile-link and website (if any)
#----------------------------------------------------------------------------------------------------
# Ideal for people looking for leads/prospects on Instagram
# Also ideal for those looking for influencers in certain fields to promote their brands
#----------------------------------------------------------------------------------------------------
import re
import csv
import time
from selenium.common.exceptions import NoSuchElementException,\
    TimeoutException,\
  WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from println import println


class Extractor:
  """
  This is where we extract all the data we need while scrapping
  We take our screenshots here, get titles, find social media pages
  Of users we extract
  """

  def __init__(self, driver, search_query, file_name):
    self._driver = driver
    self._query = search_query
    self._file_name = file_name

    self.open_initial_page()

  def open_initial_page(self):
    initial_ig_page = "https://www.instagram.com/creativeJoe007/"

    self._driver.get(initial_ig_page)
    self.search_ig()

  def search_ig(self):
    search_container = self._driver.find_element_by_css_selector(
        "div.LWmhU._0aCwM")
    search_input = search_container.find_element_by_css_selector(
        "input.XTCLo.x3qfX")

    # Clear the input should a value be present
    search_input.clear()
    time.sleep(1)
    search_input.send_keys(self._query)

    # Wait for 10sec to render the search result
    search_result_container = WebDriverWait(self._driver, 5).until(
      presence_of_element_located((By.CSS_SELECTOR, "div.drKGC"))
    )

    search_results = search_result_container.find_element_by_css_selector("div.fuqBx")\
      .find_elements_by_css_selector("a.yCE8d")

    for result in search_results:
      self._profile = {
        "url": result.get_attribute("href"),
        "image": "",
        "name": "",
        "extra_name": "",
        "bio": "",
        "followers": 0,
        "following": 0,
        "posts": 0,
        "mobile": "",
        "email": "",
        "external_links": "",
      }

      result_container = result.find_element_by_css_selector("div.z556c")

      # We check if result is a hashtag
      try:
        result_container.find_element_by_css_selector(
            "span._28KuJ.coreSpriteHashtag")
        continue
      except NoSuchElementException as e:
        pass

      # We check if result is a location
      try:
        result_container.find_element_by_css_selector(
            "div.nebtz.coreSpriteLocation")
        continue
      except NoSuchElementException as e:
        pass

      self.open_profile()
      # Save result
      self.write_to_file(self._profile)
      println(f"Finished Scrapping, {self._profile['url']}", "normal")

  def open_profile(self):
    self.window_handler("start")
    self._driver.get(self._profile["url"])

    println("-------------------------------------------------------------------------", "bold")
    println(f"Currently Scrapping, {self._profile['url']}", "bold")

    header_container = self._driver.find_element_by_css_selector("header.vtbgv")

    # Extract Images
    profile_image_container = header_container.find_element_by_css_selector("div.RR-M-")\
      .find_element_by_css_selector("span._2dbep")

    self._profile["image"] = profile_image_container.find_element_by_css_selector("img._6q-tv")\
      .get_attribute("src")

    # Extract textual data
    profile_data_container = header_container.find_element_by_css_selector("section.zwlfE")

    self._profile["name"] = profile_data_container.find_element_by_css_selector("div.nZSzR")\
      .find_element_by_css_selector("h2._7UhW9.fKFbl").text

    self.extract_profile_analytics(profile_data_container)
    self.extract_user_data(profile_data_container)
    self.extract_contact_details()

    self.window_handler("stop")

  def extract_profile_analytics(self, profile_data_container):
    # Extract things like, followers, following and total post
    user_analytics = profile_data_container.find_element_by_css_selector("ul.k9GMp")\
      .find_elements_by_css_selector("li.Y8-fY")

    # First item on the list is total post
    total_post_container = user_analytics[0]
    # Second item on the list is total followers
    total_followers_container = user_analytics[1]
    # Third item on the list is total followings
    total_following_container = user_analytics[2]
    
    self._profile["posts"] = total_post_container\
      .find_element_by_css_selector("a.-nal3")\
        .find_element_by_css_selector("span.g47SY").text

    self._profile["followers"] = total_followers_container\
      .find_element_by_css_selector("a.-nal3")\
        .find_element_by_css_selector("span.g47SY").get_attribute("title")

    self._profile["following"] = total_following_container\
      .find_element_by_css_selector("a.-nal3")\
        .find_element_by_css_selector("span.g47SY").text

  def extract_user_data(self, profile_data_container):
    user_data_container = profile_data_container.find_element_by_css_selector("div.-vDIg")

    # Extract user's nick name
    try:
      self._profile["extra_name"] = user_data_container.find_element_by_css_selector("h1.rhpdm").text
    except NoSuchElementException as e:
      pass

    # Extract user's bio
    try:
      self._profile["bio"] = user_data_container.find_element_by_tag_name("span").text
    except NoSuchElementException as e:
      pass

    # Extract user's web link
    try:
      self._profile["external_links"] = user_data_container.find_element_by_css_selector("a.yLUwa").text
    except NoSuchElementException as e:
      pass

  def extract_contact_details(self):
    # ------------------------------------------------------------------------
    # Some user's input their mobile numbers in their bio
    # Some, upload whatsapp link they can be contacted from
    # Same goes with email
    # We decided to search for this data from both places
    # ------------------------------------------------------------------------
    bio = self._profile["bio"]
    external_link_text = self._profile["external_links"]

    mobile_present_in_bio: list = self.extract_mobile_number(bio)
    email_present_in_bio: list = self.extract_email_address(bio)

    mobile_present_in_external_link: list = self.extract_mobile_number(external_link_text)
    email_present_in_external_link: list = self.extract_email_address(external_link_text)

    # Join both results into one
    self._profile["mobile"] = mobile_present_in_bio + mobile_present_in_external_link
    self._profile["email"] = email_present_in_bio + email_present_in_external_link
    

  def extract_mobile_number(self, source: str) -> list:
    found_numbers: list = []
    phone_regex = "[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]"

    is_found = re.findall(phone_regex, source, re.IGNORECASE)
    if len(is_found) > 0:
      if type(is_found[0]) is tuple:
        # ------------------------------------------------------------------------
        # Our second regex returns a tuple instead of a string like the other one
        # I haven't figured how to resolve that but this is just a work around
        # ------------------------------------------------------------------------
        found_numbers = [is_found[0][0]]
      else: found_numbers = is_found
    
    return found_numbers

  def extract_email_address(self, source: str) -> list:
    extracted_email_addresses: list = []
    email_regex = "[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*"
    emails_found = re.findall(email_regex, source, re.IGNORECASE)

    return emails_found

  def window_handler(self, action):
    if action =="start":
      self._driver.execute_script("window.open('');")
      self._driver.switch_to.window(self._driver.window_handles[len(self._driver.window_handles) - 1])

    else:
      self._driver.close()
      self._driver.switch_to.window(self._driver.window_handles[len(self._driver.window_handles) - 1])


  def write_to_file(self, data: dict):
    # ------------------------------------------------------------------------
    # We check if the file already exist before we being, if the file
    # Exist, we simply append the new data as the header for the CSV file has
    # Already be created
    # Else we add CSV header first before adding the data to file
    # ------------------------------------------------------------------------
    extracted_path = Path("extracted/")
    save_file_to = extracted_path / f"{self._file_name}.csv"
    file_path_object = Path(save_file_to)
    file_exist = file_path_object.is_file()
    if file_exist is False:
      Path(save_file_to).touch()

    with open(save_file_to, 'a', newline='') as file:
        writer = csv.writer(file, delimiter='|')
        # Add header only if the file doesn't exist
        if file_exist is False: writer.writerow(data.keys())
        # Add new data 
        writer.writerow(data.values())
        file.close()
      