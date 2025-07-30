import time
from patchright.sync_api import sync_playwright

def bypass_shadow_root(page):
    inputs = page.query_selector_all('input')
    for input_elem in inputs:
        try:
            attrs = input_elem.evaluate('''el => ({
                name: el.getAttribute('name'),
                type: el.getAttribute('type')
            })''')

            if attrs.get('name') and 'turnstile' in attrs.get('name') and attrs.get('type') == 'hidden':
                parent = input_elem.evaluate_handle('el => el.parentElement')
                print("ppppppp", parent) # working till here
                parent_shadow = parent.evaluate_handle('el => el.shadowRoot') # failed
                # no root found here. mp because of closed shadow root 
                
                if not parent_shadow or not parent_shadow.evaluate('el => el !== null'):
                    continue

                body_element = parent_shadow.evaluate_handle('el => el.querySelector("body")')
                body_shadow = body_element.evaluate_handle('el => el.shadowRoot')

                if body_shadow:
                    button = body_shadow.evaluate_handle('el => el.querySelector("input")')
                    if button and button.evaluate('el => el !== null'):
                        return button
        except:
            continue
    return None

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="data",
            channel="chrome",
            headless=False,
            no_viewport=True,
        )
        page = browser.new_page()
        page.goto("https://nopecha.com/demo/cloudflare")
        time.sleep(15)
        while(True):
            button = bypass_shadow_root(page)
            button.click()
main()
