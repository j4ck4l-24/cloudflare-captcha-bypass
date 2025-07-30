from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.errors import ElementLostError, ContextLostError
import time

def bypass_cloudflare_protection():
    options = ChromiumOptions()
    options.set_argument('--incognito')
    browser = ChromiumPage(options)
    browser.get('https://www.crunchbase.com/browser-extension-captcha')
    
    for _ in range(10):
        try:
            time.sleep(1)
            cookies = browser.cookies()
            cf_clearance = None  

            for c in cookies:
                if c["name"] == "cf_clearance":
                    cf_clearance = c["value"]
            if cf_clearance:
                print("cf_clearance:", cf_clearance)
                browser.close()
                return True

            for element in browser.eles("tag:input"):
                try:
                    attrs = element.attrs
                    if attrs.get("name", "") == "cf-turnstile-response":
                        try:
                            container_div = element.parent()
                            print("cccc", container_div) # verified till here and working
                            initial_shadow_root = container_div.shadow_root.child()
                            print("sss", initial_shadow_root) # verified and iframe loaded with correct challenge. body --> input[checkbox] should be next
                            body = initial_shadow_root("tag:body")
                            # print("bbbbb", body) nothing getting printed
                            button = body.shadow_root("tag:input")
                            if button:
                                button.click()
                                time.sleep(3)
                                break
                        except (ElementLostError, ContextLostError):
                            break
                except (ElementLostError, ContextLostError):
                    continue

            time.sleep(2)

        except (ElementLostError, ContextLostError):
            time.sleep(2)
        except Exception:
            time.sleep(2)

    return False

bypass_cloudflare_protection()
