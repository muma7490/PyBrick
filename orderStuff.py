from selenium.webdriver import Chrome,Firefox
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
opts = Options()

#opts.set_headless()

#assert opts.headless

def clickButton(browser):
    button_area = browser.find_elements_by_css_selector('div.l-margin-top')
    button_area = button_area[4]
    button = button_area.find_element_by_css_selector('button.bl-btn.primaryGreen')
    try:
        button.click()
    except Exception as e:
        print("failed to click")
        print(e)
        raise e

def fillQty(browser):
    qtyform = browser.find_element_by_class_name('addToCartQty')
    try:
        qtyform.clear()
        qtyform.send_keys(qty)
    except:
        print("failed to fill qty, retry")
        print(e)
        raise e


def order(browser):
    str.replace(qty, "\n", "")

    print("URL : " + url + ", qty: " + qty)

    browser.get(url)

    try:
        fillQty(browser)
    except:
        fillQty(browser)

    try:
        clickButton(browser)
    except:
        clickButton(browser)

    browser.find_element_by_css_selector('div.text.success')

browser = Chrome(options=opts)
browser.implicitly_wait(5)

items = []
with open("best.order",'r') as f:
    items = f.readlines()

failedlist = []

cnt = 0
emptyLines = 0

for i in items:

    try:
        url,qty,id = i.split("|")
    except ValueError:
        emptyLines+=1
        print("line is "+i)
        continue

    try:
        str.replace(qty,"\n","")
        print("URL : "+url+", qty: "+qty, ", part is"+id)
    except Exception as e:
        print("Failed to parse url!")
        raise e

    browser.get(url)
    try:
        try:
            order(browser)
        except Exception as e:
            print("First order failed, retry")
            print(e)
            order(browser)
    except Exception as e:
        print("------------------------------------------------------------------------------------")
        print("failed to order! Please repeat manually")
        print(e)
        print(i)
        failedlist.append(i)
        print("------------------------------------------------------------------------------------")
        continue
    cnt +=1


print("MISSING STUFF:")
for i in failedlist:
    url, qty,id = i.split("|")
    print("URL : " + url + ", qty: " + qty + ", id: "+id)

print("Done: "+str(cnt))
print("Missing: "+str(len(failedlist)))
print("Total: "+str(cnt + len(failedlist)))
print("Expected: "+str(len(items)-emptyLines))