from apscheduler.schedulers.background import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import subprocess
import time

# ==== USER CONFIG BIT ====

# define products to check for by their product code(s)
product_codes = ['30183989',
                 '10277984',
                 '80256940',
                 '20246402']

# define the serach URL (up to and including "q="). The one below is suitable for UK searches, other nationalities will have different URLs
search_url = "https://www.ikea.com/gb/en/search/products/?q="

# define hours of the day to check stock
check_times = '9,13,17'

# ==== END USER CONFIG ====


# instantiate APScheduler
sched = BlockingScheduler()

# set options for browser being used by Selenium for web requests
chrome_options = Options()  
chrome_options.add_argument("--headless") 

# Function that gives OS notification when items are in stock (the one below is for MacOS)
def os_notifier(in_stock_count, product_codes, not_founds):
    if in_stock_count == len(product_codes):
        # Raises an MacOS notification if *all* items are in stock
        subprocess.run('terminal-notifier -message "All Ikea items in stock" -title "Go buy Ikea stuff!!"', shell=True)
    elif in_stock_count == len(product_codes) - not_founds:
        # Raises an OS notification is all items that could be returned in a search were in stock
        subprocess.run('terminal-notifier -message "All found Ikea items are in stock" -title "Maybe buy Ikea stuff"', shell=True)

""" # if using Windows remove the "os_notifier" function above and replace it with the one below
def os_notifier(in_stock_count, prod_codes, not_founds):
    import win10toast
    n = ToastNotifier()
    if in_stock_count == len(product_codes):
        # Raises an MacOS notification if *all* items are in stock
        n.show_toast("All items in stock", "Go buy Ikea stuff!", duration = 60)
    elif in_stock_count == len(product_codes) - not_founds:
        # Raises an OS notification is all items that could be returned in a search were in stock
        n.show_toast("All found items are in stock", "All Ikea items that could be found are in stock", duration = 60)
"""

def searcher(prod_code, driver):
    #full_search_url = f"https://www.ikea.com/gb/en/search/products/?q={prod_code}"
    full_search_url = search_url + prod_code
    driver.get(full_search_url)
    time.sleep(0.25)  # short sleep after 'get' seems to lessen occurances of failed stock checks
    search_results = driver.find_elements_by_class_name("search-summary__content")
    for result in search_results:
        #print(result.text.strip())
        if "Oh no! We couldn't find a single match for" in result.text.strip():
            # it ain't there! The item doesn't exist on the website (discontinued / temporarily removed from product lineup)
            return 1
        else:
            status=1
            while status > 0:
                links = driver.find_elements_by_css_selector("div.range-revamp-product-compact__bottom-wrapper a")
                for link in links:
                    # always only expect 1 result when searching on product code
                    prod_page = link.get_attribute("href")
                    #print(prod_page)
                    driver.get(str(prod_page))
                    time.sleep(0.25)  # short sleep after 'get' seems to lessen occurances of failed stock checks
                    online_stockcheck = driver.find_elements_by_class_name("range-revamp-stockcheck__text")
                    for item in online_stockcheck:
                        if "Currently unavailable" in item.text.strip():
                            # "out of stock"
                            status=0
                            return 2
                        else:
                            # "In Stock"
                            status=0
                            return 3
                status+=1
                # IF to prevent infinite loop
                if status == 40:
                    return 4

def stock_checker():
    driver = webdriver.Chrome(options=chrome_options)
    print(f'####   AT: {datetime.now()}   ####')
    print(' __________________________________________')
    print('|  Product   |  In Stock  |  Status        |')
    print(' ==========================================')
    in_stock_count = 0
    not_founds = 0
    for code in product_codes:
        result = searcher(code, driver)
        if result == 1:
            print(f'|  {code}  |     N      |  Not Found     |')
            not_founds += 1
        elif result == 2:
            print(f'|  {code}  |     N      |  Out of stock  |')
        elif result == 3:
            print(f'|  {code}  |    YES     |  In Stock      |')
            in_stock_count += 1
        elif result == 4:
            print(f'|  {code}  |   * stock check failed *    |')
        else:
            print('well, how did we get here?!')
            print(result)
    print(' ==========================================')
    print('\n')
    # The following IF gives calls an OS notification if the stock is in
    if in_stock_count == len(product_codes) or in_stock_count == len(product_codes) - not_founds:
        os_notifier(in_stock_count, product_codes, not_founds)
    driver.quit()


# initial check run at start, then onto scheduled times
print('\n')
stock_checker()

# Scheduling of stock checks
sched.add_job(stock_checker, 'cron', hour=check_times, misfire_grace_time=900)
sched.start()
