from playwright.sync_api import sync_playwright
import json
import time


def scrape_india_women_latest_match():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set True for silent mode
        page = browser.new_page()

        # Step 1: Open Cricbuzz
        page.goto("https://www.cricbuzz.com/")
        page.wait_for_load_state("networkidle")
        print("✅ Opened Cricbuzz homepage")

        # Step 2: Click the "India Women" button
        try:
            # Usually under the "Teams" section at the top
            india_women_button = page.locator("a[href*='/cricket-team/india-women/']")
            india_women_button.first.click()
            print("🇮🇳 Clicked 'India Women' team page")
        except Exception as e:
            print(f"❌ Could not find 'India Women' button: {e}")
            browser.close()
            return

        # Step 3: Wait for India Women team page to load
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Step 4: Click on the latest match (first visible match card)
        try:
            latest_match = page.locator("a.cb-mtch-lst.cb-col.cb-col-100.cb-tms-itm").first
            match_url = latest_match.get_attribute("href")
            full_url = f"https://www.cricbuzz.com{match_url}"
            print(f"🏏 Opening latest match: {full_url}")
            page.goto(full_url)
        except Exception as e:
            print(f"❌ Could not find the latest match link: {e}")
            browser.close()
            return

        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Step 5: Go to the Scorecard tab
        try:
            scorecard_tab = page.locator("a[href*='scorecard']").first
            scorecard_tab.click()
            print("📊 Opened the Scorecard tab")
        except Exception as e:
            print(f"❌ Could not open Scorecard tab: {e}")
            browser.close()
            return

        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Step 6: Extract scorecard data
        print("📥 Extracting scorecard data...")
        innings = page.locator(".cb-col.cb-col-100.cb-ltst-wgt-hdr")
        score_data = []

        for i in range(innings.count()):
            inning = innings.nth(i)
            title = inning.locator(".cb-col.cb-col-100.cb-scrd-hdr-rw").inner_text()
            print(f"\nInning: {title}")

            players = inning.locator(".cb-scrd-itms")
            inning_data = {"inning": title, "players": []}

            for j in range(players.count()):
                row = players.nth(j).inner_text().strip()
                if row:
                    inning_data["players"].append(row)

            score_data.append(inning_data)

        # Step 7: Save to a file
        with open("india_women_latest_scorecard.json", "w", encoding="utf-8") as f:
            json.dump(score_data, f, indent=4)

        print("✅ Scorecard data saved to 'india_women_latest_scorecard.json'")

        browser.close()


if __name__ == "__main__":
    scrape_india_women_latest_match()
