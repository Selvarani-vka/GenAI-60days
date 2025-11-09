import asyncio
from playwright.async_api import async_playwright
import csv

async def fetch_scorecard():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Open Cricbuzz homepage
        await page.goto("https://www.cricbuzz.com/", timeout=40000)

        # 2. Click India Women button
        await page.wait_for_selector("xpath=/html/body/div/main/div[2]/div[2]/div/a[4]", timeout=10000)
        await page.click("xpath=/html/body/div/main/div[2]/div[2]/div/a[4]")
        await page.wait_for_timeout(4000)

        # 3. Click Results tab
        await page.wait_for_selector("a:has-text('Results')", timeout=10000)
        await page.click("a:has-text('Results')")
        await page.wait_for_timeout(4000)

        # 4. Click the first match link
        await page.wait_for_selector("xpath=/html/body/div/main/div[2]/div[1]/div/div/div[2]/div/div/div[1]/a/span", timeout=15000)
        await page.click("xpath=/html/body/div/main/div[2]/div[1]/div/div/div[2]/div/div/div[1]/a/span")
        await page.wait_for_timeout(4000)

        # 5. Click Scorecard tab
        await page.wait_for_selector("a:has-text('Scorecard')", timeout=10000)
        await page.click("a:has-text('Scorecard')")
        await page.wait_for_timeout(5000)

        # 6. Extract batter rows using your exact scorecard XPath
        scorecard_container = page.locator("xpath=/html/body/div/main/div/div[2]/div[1]/div/div/div[3]/div[1]")

        batter_rows = scorecard_container.locator("xpath=.//div[contains(@class, 'cb-col') and contains(@class, 'cb-scrd-itms')]")

        batter_rows_count = await batter_rows.count()
        print(f"Found {batter_rows_count} batter rows inside scorecard container.")

        rows_data = []

        for i in range(batter_rows_count):
            row = batter_rows.nth(i)
            cells = row.locator("div")
            cells_count = await cells.count()
            cell_texts = [await cells.nth(j).inner_text() for j in range(cells_count)]

            print(f"Row {i + 1} data: {cell_texts}")

            # Filter for rows with 6+ cells (likely batter rows)
            if len(cell_texts) >= 6:
                rows_data.append(cell_texts[:6])

        # 7. Save to CSV
        csv_filename = "india_women_scorecard.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Batter", "R", "B", "4s", "6s", "SR"])
            writer.writerows(rows_data)

        print(f"✅ Scorecard data saved to {csv_filename}")

        await browser.close()

asyncio.run(fetch_scorecard())
