# Ikea Checker

I recently wanted to get a modular wardobe from Ikea. Problem is that there are lots of individual componets which never seemed to be in stock all at once. Getting stuff delivered from Ikea is expensive, so you want to make sure you can do it in one go, but then manually checking every part manually take ages. So I wrote a script to check the online stock levels for me. I was using it for 3 weeks before what I needed all came in stock, so this simple little script saved me _hours_!

The script checks Ikea 3 times a days to see if all the items are in stock *online* (this does not check store stock levels), and when they are, you'll get an operating system desktop notification.


## Setup

As Ikea dynamically creates its web pages it is not not possible to do simple web scraping. Instead, it is necessary to render the pages so that the dynamiic content can be recovered. This requires use of Selemium, which renders the content in a Chrome window (hidden in the background in this script). So, the first step is to install Chrome if you don't have it already. The second step is to install the ChromeDriver that gives Selenium access to the browser:

MacOS install instructions:
[http://jonathansoma.com/lede/foundations-2017/classes/more-scraping/selenium/](http://jonathansoma.com/lede/foundations-2017/classes/more-scraping/selenium/)
Windows install instructions:
[http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/)

Make sure you get the right version of ChromeDriver to go with your version of Chrome.

Then you'll need to setup the virtual environment in which to run the script, and install the requirements. Run the following in the directory you download the scriipt to

```bash
python3 -m venv venv
source venv/biin/activate
pip install -r requirements.txt
```

Note: if using a Mac, you should expect the installation of win10toast to fail (this is only required if running on Windows)

You'll need to run the "source venv/bin/activate" command before you run the script whenever you're using a fresh terminal window to run the script.


## Windows customisation

The script is already setup for Mac, but if you're using Windows the function that provides a system notification when your items are in stock is different to what is used on a Mac. I've been really lazy, and have not written any logic to identify what OS you're using, so there's some manual editing to do to the script before using it if you're on Windows. You will need to:

1. Remove or comment out the "os_notifier" function that is currently on lines 42-49
2. Uncomment the "os_notifier" function between lines 51 and 61

I can't guarantee it'll work. It's completely untested, but there's not much to it, so... hopefully it's fine!


## Script customisations

At the top of the script there's a section where you can customise what the script's looking for and how it does it

```Python
# ==== USER CONFIG BIT ====

# define products to check for by their product code(s)
product_codes = ['30183989',
                 '10277984']

# define the serach URL (up to and including "q="). The one below is suitable for UK searches, other nationalities will have different URLs
search_url = "https://www.ikea.com/gb/en/search/products/?q="

# define hours of the day to check stock
check_times = '9,13,17'

# ==== END USER CONFIG ====
```

There are 3 variable to change here:

1. product_codes: This is a list of strings which represent the product code(s) that you want to perform the stock check on. Product codes are all 8 digit numbers that are most easily found from the product page's URL. For example, if a Billy Bookcase's URL is 'https://www.ikea.com/gb/en/p/billy-bookcase-white-50263838/', the product code is '50263838'. Create a list of these product code for the checker to check.

2. search_url: This is the URL on the search results page, minus the search term. The URL above is the UK's Ikea search URL. If you're not in the UK your search URL will probably differ from this (particualrly the '/gb/en/' part of the URL).

3. check_times: The hours of the day which to check the website for stock updates. Please don't abuse this - website owners do not like excessive requests clogging up their sites, and there's really no need to be checking the site more than 3 times a day.


## Run the script

With your virtual environment active, run the command below:

```Bash
python ikea_check.py
```

The script will perform one immediate stock check, whose result will be visible in the terminal. After that you can just leave it running and it will run another check next time one is scheduled, and will continue to do so for as long as it's running.

Once all items are in stock, or all items that can be returned in a search are in stock you will receive a notificationi on your OS, and you can go and buy the stuff you want.


## Error?

If you get this error

```This version of ChromeDriver only supports Chrome version XX```

You need a new version of ChromeDriver. Follow the link below for instructions:

Mac: [http://jonathansoma.com/lede/foundations-2017/classes/more-scraping/selenium/](http://jonathansoma.com/lede/foundations-2017/classes/more-scraping/selenium/)
Win: [http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/)
