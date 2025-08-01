from patchright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    context.clear_cookies()

    page.goto('https://www.crunchbase.com/browser-extension-captcha')
    time.sleep(5) 


    while True:
        try:
            page.focus("body")
        except:
            print("errorrrrr")
        page.keyboard.press("Tab")
        time.sleep(0.1)
        page.keyboard.press("Space")
        cookies = context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'cf_clearance':
                print(cookie)
                browser.close()
                exit()
                break
        time.sleep(2)
