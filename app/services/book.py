import requests
from typing import Dict, Any, Optional
from openai import OpenAI
from app.core.config import get_settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

settings = get_settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def _parse_volume_info(volume: Dict[str, Any]) -> Dict[str, Any]:
  """Helper function to parse volume information from Google Books API response"""
  volume_info = volume.get("volumeInfo", {})
  return {
		"id": volume.get("id"),
		"volumeInfo": {
			"title": volume_info.get("title", "Unknown Title"),
			"subtitle": volume_info.get("subtitle"),
			"authors": volume_info.get("authors", []),
			"publisher": volume_info.get("publisher"),
			"publishedDate": volume_info.get("publishedDate"),
			"description": volume_info.get("description"),
			"industryIdentifiers": volume_info.get("industryIdentifiers", []),
			"pageCount": volume_info.get("pageCount"),
			"categories": volume_info.get("categories", []),
			"averageRating": volume_info.get("averageRating"),
			"ratingsCount": volume_info.get("ratingsCount"),
			"imageLinks": volume_info.get("imageLinks", {}),
			"language": volume_info.get("language"),
			"previewLink": volume_info.get("previewLink"),
			"infoLink": volume_info.get("infoLink")
		}
}

def search_books(query: str, lang: Optional[str] = None, max_results: int = 10):
	"""Search for books using the Google Books API"""
	url = "https://www.googleapis.com/books/v1/volumes"
	params = {
		"q": query,
		"key": settings.GOOGLE_BOOKS_API_KEY,
		"langRestrict": lang,
		"maxResults": max_results
	}
	
	response = requests.get(url, params=params)
	response.raise_for_status()
	data = response.json()
	
	return {
		"books": [_parse_volume_info(item) for item in data.get("items", [])],
		"totalItems": data.get("totalItems", 0)
	}

def get_book_details(book_id: str):
	"""Get detailed information about a specific book"""
	url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
	params = {"key": settings.GOOGLE_BOOKS_API_KEY}
	
	response = requests.get(url, params=params)
	response.raise_for_status()
	return _parse_volume_info(response.json())


def parse_toc_to_json(toc_text):
	lines = toc_text.split("\n")
	toc = []

	for line in lines:
			# Determine type and extract details
			if re.match(r"^Part\s\d+", line, re.IGNORECASE):  # Section title
					toc.append({"type": "section", "title": line.strip(), "page": None})
			elif re.match(r"^\d+", line):  # Chapter title
					match = re.match(r"^(\d+)\s+(.*?)\s+(\d+)$", line)
					if match:
							toc.append({
									"type": "chapter",
									"number": int(match.group(1)),
									"title": match.group(2).strip(),
									"page": int(match.group(3))
							})
			elif "Timeline" in line or "Introduction" in line:  # Intro
					toc.append({"type": "intro", "title": line.strip(), "page": None})
			else:  # Other
					toc.append({"type": "other", "title": line.strip(), "page": None})

	return {"toc": toc}


def scrape_toc_from_bn(book_title, author_name):
	chrome_options = Options()
	chrome_options.add_argument("--headless") 
	chrome_options.add_argument("--no-sandbox")  
	chrome_options.add_argument("--disable-dev-shm-usage")  
	chrome_options.add_argument("--disable-gpu")  
	chrome_options.add_argument("--start-maximized")  
	chrome_options.add_argument("--window-size=1920,1080")
	chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") 

	# Set up the Chrome WebDriver
	driver = webdriver.Chrome(
		service=Service(ChromeDriverManager().install()), options=chrome_options
	)

	try:
		# Step 1: Search for the book on Barnes & Noble
		search_query = f"{book_title} {author_name}".replace(" ", "+")
		search_url = f"https://www.barnesandnoble.com/s/{search_query}"
		driver.get(search_url)
		print(f"Accessing... {search_url}")

		# Step 2: Wait for search results and locate the first book link
		try:
			WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.CLASS_NAME, "pImageLink"))
			)
			book_link = driver.find_element(By.CLASS_NAME, "pImageLink")
			book_url = book_link.get_attribute("href")
			print(f"✅ Book Page URL found: {book_url}")
		except Exception as e:
			return f"❌ Error: Could not find book link on search results. {e}"
		
		# Step 3: Navigate to the book detail page
		driver.get(book_url)
		WebDriverWait(driver, 20).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='#TOC']"))
		)
		print("✅ Table of Contents Tab Found")

		# Step 4: Click the "Table of Contents" tab
		try:
			toc_tab = driver.find_element(By.CSS_SELECTOR, "a[href='#TOC']")
			print("Html: ", toc_tab.get_attribute("outerHTML"))
			driver.execute_script("arguments[0].click();", toc_tab)
			print("✅ Clicked on the 'Table of Contents' tab via JavaScript.")
			# time.sleep(3)  # Wait for content to load
		except Exception as e:
			return f"❌ Error: Could not find or click the 'Table of Contents' tab. {e}"
		

		# Step 5: Click on the show more button
		try:
			show_more_button = driver.find_element(By.CSS_SELECTOR, "a.read-more.show-more-pdp")
			driver.execute_script("arguments[0].click();", show_more_button)
			print("✅ Clicked on the 'Show More' button.")
		except Exception as e:
			return f"❌ Error: Could not find or click the 'Show More' button. {e}"


		# Step 6: Extract the Table of Contents
		try:
			WebDriverWait(driver, 20).until(
				EC.visibility_of_element_located((By.CSS_SELECTOR, "div.d-sm-block.table-of-contents.centered"))
			)
			toc_section = driver.find_element(By.CSS_SELECTOR, "div.d-sm-block.table-of-contents.centered")
			toc_text = toc_section.text.strip()
			return toc_text if toc_text else "No Table of Contents found."
		except Exception as e:
			return f"❌Error: Could not extract the 'Table of Contents'. {e}"

	except Exception as e:
		return f"Error occurred: {e}"

	finally:
		# Close the WebDriver
		driver.quit()

