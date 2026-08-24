import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

TARGETS = [
    {
        "slug": "hdfc_midcap",
        "url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth"
    },
    {
        "slug": "hdfc_smallcap",
        "url": "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
    },
    {
        "slug": "hdfc_gold_fof",
        "url": "https://groww.in/mutual-funds/hdfc-gold-etf-fund-of-fund-direct-plan-growth"
    },
    {
        "slug": "hdfc_largecap",
        "url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
    },
    {
        "slug": "hdfc_elss",
        "url": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
    }
]

async def scrape_scheme(page, target):
    url = target["url"]
    slug = target["slug"]
    
    print(f"Scraping {slug} from {url}...")
    await page.goto(url, wait_until="domcontentloaded")
    
    # Wait for the main content to load (adjust timeout if necessary)
    try:
        await page.wait_for_selector("table", timeout=10000)
    except Exception:
        print(f"  Warning: table not found quickly on {slug}, continuing anyway...")
        
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")
    
    # Try to remove script and style elements
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
        
    # Get all text
    text_content = soup.get_text(separator="\n", strip=True)
    
    # Clean up empty lines
    lines = [line.strip() for line in text_content.split('\n') if line.strip()]
    cleaned_text = '\n'.join(lines)
    
    # Ensure directory exists
    dir_path = os.path.join("data", "raw", slug)
    os.makedirs(dir_path, exist_ok=True)
    
    # Save the scraped text
    info_path = os.path.join(dir_path, "scheme_info.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
        
    # Save metadata
    meta_path = os.path.join(dir_path, "metadata.json")
    metadata = {
        "slug": slug,
        "source_url": url,
        "scrape_date": datetime.utcnow().isoformat() + "Z"
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"  Saved {slug} data. ({len(cleaned_text)} characters)")

async def main():
    async with async_playwright() as p:
        # Using headless mode
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for target in TARGETS:
            try:
                await scrape_scheme(page, target)
                # Wait a bit between requests to avoid rate limits
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error scraping {target['slug']}: {e}")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
