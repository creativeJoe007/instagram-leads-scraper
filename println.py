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
import os

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def println(text, _type='fail'):
  # os.system('color')
  if _type == 'fail':
    print(f"\n{FAIL} {text} {ENDC}\n")
  elif _type == 'success':
    print(f"\n{OKGREEN} {text}  {ENDC}\n")
  elif _type == 'normal':
    print(f"\n{OKBLUE} {text}  {ENDC}\n")
  elif _type == 'bold':
    print(f"\n{BOLD} {text}  {ENDC}\n")
  elif _type == 'warn':
    print(f"\n{WARNING} {text}  {ENDC}\n")