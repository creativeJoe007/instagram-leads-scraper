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

import argparse
from browser import determine_browser
from extractor import Extractor
from println import println

arguments = argparse.ArgumentParser()

arguments.add_argument('search', action='store', type=str, help="This is your instagram search query")
arguments.add_argument('--file', action='store', type=str, required=True, help="File name to save extracted data")
arguments.add_argument('--browser', action='store', type=str, required=False, default="chrome", help="What browser should we\
   scrape with?")
arguments.add_argument('--driver', action='store', type=str, required=False, help="Browser executable path")

args = arguments.parse_args()


def main():
	search_query: str = args.search
	file_name: str = args.file
	selected_browser: str = args.browser
	browser_driver_path: str = args.driver

	driver = determine_browser(selected_browser, browser_driver_path)
	if type(driver) == str:
		println(driver)
	else:
		println(f"Instagram's Search Query: {search_query}", "normal")
		extractor = Extractor(driver, search_query, file_name)
		driver.close()

main()

