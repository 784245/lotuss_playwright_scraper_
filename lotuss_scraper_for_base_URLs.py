import random

from playwright.async_api import async_playwright
import pandas as pd

async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=False)
        page=await browser.new_page()

        await page.goto("https://www.lotuss.com.my/en/category/grocery/sundry?sort=relevance:DESC",timeout=200000)


        hrefs = []
        while True:
            for i in range(8):
                await page.keyboard.press('PageDown')
                await asyncio.sleep(random.randint(8, 14))

            xpath="//div[@class='sc-bSqaIl DTxkj']/a"
            count=await page.locator(xpath).count()
            for i in range(count):

                href=await page.locator("//div[@class='sc-bSqaIl DTxkj']/a").nth(i).get_attribute('href')
                hrefs.append(href)
                print(href)
            print(len(hrefs))
            try:
                await page.click('//a[@title="Next page"]')
                await asyncio.sleep(7)
            except:
                print("no more links")
                break
        df = pd.DataFrame(hrefs)
        df.to_csv('sundry.csv', index=False)

        await browser.close()

import asyncio
asyncio.run(main())