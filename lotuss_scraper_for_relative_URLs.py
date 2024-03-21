import pandas as pd
from playwright.async_api import async_playwright
import random

async def main():
    data = {
        "Product_Title": [],
        "Price": [],
        "Image_URL": [],
        "Product_URL": [],
        "Product_Information": [],
    }
    try:

        async with async_playwright() as p:

            browser=await p.chromium.launch(headless=False)
            page=await browser.new_page()


            links=pd.read_csv("sundry.csv",header=None,skiprows=2)

            for link in links[0]:
                url="https://www.lotuss.com.my" + link
                print(url)
                await page.goto(url)
                # await asyncio.sleep(random.randint(,10))
                # for i in range(random.randint(1,2)):
                #     await page.keyboard.press("ArrowDown")
                selector_timeout = 25000
                # await page.wait_for_selector('xpath=/html/body/div[1]/div/div[1]/div[3]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div/div',timeout=selector_timeout)


                # Extracting product details
                try:
                    product_title_selector = 'xpath=/html/body/div[1]/div/div[1]/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[1]/h1'
                    await page.wait_for_selector(product_title_selector, timeout=selector_timeout)
                    title=await page.text_content(product_title_selector)
                    data["Product_Title"].append(title)
                    # print(title)
                except Exception as e:
                    print("Error extracting product title:", e)
                    data["Product_Title"].append(None)

                try:
                    price_selector = "xpath=/html/body/div[1]/div/div[1]/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div"
                    await page.wait_for_selector(price_selector, timeout=selector_timeout)
                    price=await page.text_content(price_selector)
                    data["Price"].append(price)
                    # print(price)
                except Exception as e:
                    print("Error extracting product price:", e)
                    data["Price"].append(None)

                try:
                    image_url_selector = 'xpath=//img[@id="current-product-image"]'
                    await page.wait_for_selector(image_url_selector, timeout=selector_timeout)
                    image=await page.locator(image_url_selector).get_attribute('src')
                    data["Image_URL"].append(image)
                    # print(image)
                except Exception as e:
                    print("Error extracting product image URL:", e)
                    data["Image_URL"].append(None)

                try:
                    description_selector = 'xpath=/html/body/div[1]/div/div[1]/div[3]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div/div'
                    await page.wait_for_selector(description_selector, timeout=selector_timeout)
                    data["Product_Information"].append(await page.inner_text(description_selector))
                except Exception as e:
                    print("Error extracting product description:", e)
                    data["Product_Information"].append(None)

                data["Product_URL"].append(page.url)
                # print(data)
            await browser.close()

    except Exception as e:
        print(f"An error occurred while setting up or closing the browser: {str(e)}")
    df = pd.DataFrame(data)
    df.to_csv("sundry_products.csv", index=False)



import asyncio
asyncio.run(main())


