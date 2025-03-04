import requests
from PIL import Image
from io import BytesIO
import webbrowser
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from fpdf import FPDF
import os

# Initialize rich console
console = Console()

# Cache for storing API responses
cache = {}

# Supported languages and their descriptions
LANGUAGE_DESCRIPTIONS = {
    "en": {"name": "English", "description": "Uses the Latin alphabet with 26 letters. Language code: 'en'."},
    "es": {"name": "Spanish", "description": "Uses the Latin alphabet with additional characters like 'ñ'. Language code: 'es'."},
    "zh": {"name": "Chinese", "description": "Uses logograms (characters) representing words or morphemes. Language code: 'zh'."},
    "hi": {"name": "Hindi", "description": "Uses the Devanagari script with 48 characters. Language code: 'hi'."},
    "ar": {"name": "Arabic", "description": "Uses the Arabic script, written from right to left. Language code: 'ar'."},
    "fr": {"name": "French", "description": "Uses the Latin alphabet with diacritics like 'é' and 'ç'. Language code: 'fr'."},
    "ja": {"name": "Japanese", "description": "Uses a combination of Kanji, Hiragana, and Katakana scripts. Language code: 'ja'."},
    "ru": {"name": "Russian", "description": "Uses the Cyrillic alphabet with 33 letters. Language code: 'ru'."},
}

def fetch_wikipedia_summary(search_term, lang="en"):
    cache_key = f"summary_{lang}_{search_term}"
    if cache_key in cache:
        return cache[cache_key]

    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{search_term.replace(' ', '_')}"
    headers = {
        "User-Agent": "GeneralInfoFetcher/1.0 (https://github.com/yourusername/yourrepository; your.email@example.com)"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        summary = data.get("extract", "No summary available.")
        cache[cache_key] = summary
        return summary
    except requests.exceptions.RequestException as err:
        return f"Failed to fetch Wikipedia summary: {err}"

def fetch_image(search_term, lang="en"):
    cache_key = f"image_{lang}_{search_term}"
    if cache_key in cache:
        return cache[cache_key]

    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&titles={search_term}&prop=pageimages&format=json&pithumbsize=500"
    headers = {
        "User-Agent": "GeneralInfoFetcher/1.0 (https://github.com/yourusername/yourrepository; your.email@example.com)"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "thumbnail" in page:
                image_url = page["thumbnail"]["source"]
                image_response = requests.get(image_url, headers=headers)
                image_response.raise_for_status()
                image = Image.open(BytesIO(image_response.content))
                cache[cache_key] = image
                return image
        return None
    except requests.exceptions.RequestException as err:
        console.print(f"⚠️ Failed to fetch image: {err}", style="bold red")
        return None

def open_wikipedia_page(search_term, lang="en"):
    url = f"https://{lang}.wikipedia.org/wiki/{search_term.replace(' ', '_')}"
    try:
        webbrowser.open(url)
        console.print(f"🌐 Opening Wikipedia page for {search_term}...", style="bold blue")
    except Exception as err:
        console.print(f"⚠️ Failed to open Wikipedia page: {err}", style="bold red")

def export_to_pdf(search_term, summary, image):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Summary about {search_term}", ln=True, align="C")
    pdf.multi_cell(0, 10, txt=summary)
    if image:
        image_path = f"{search_term}_image.png"
        image.save(image_path)
        pdf.image(image_path, x=10, y=pdf.get_y(), w=180)
        os.remove(image_path)
    pdf.output(f"{search_term}_summary.pdf")
    console.print(f"📄 Exported summary and image to {search_term}_summary.pdf", style="bold green")

def display_language_descriptions():
    table = Table(title="🌍 Language Descriptions")
    table.add_column("Language Code", style="cyan", no_wrap=True)
    table.add_column("Language Name", style="magenta")
    table.add_column("Description", style="green")

    for code, info in LANGUAGE_DESCRIPTIONS.items():
        table.add_row(code, info["name"], info["description"])

    console.print(table)

def display_info(search_term, lang="en"):
    # Fetch summary from Wikipedia
    print("\t")
    wikipedia_summary = fetch_wikipedia_summary(search_term, lang)
    console.print(Panel.fit(Text(f"Summary about {search_term}", style="bold green")))
    print("\t")
    console.print(wikipedia_summary)

    # Fetch and display image
    image = fetch_image(search_term, lang)
    if image:
        console.print("\n🖼️ Displaying image...", style="bold blue")
        image.show()
    else:
        console.print("\n⚠️ No image available.", style="bold red")

    # Ask if the user wants to know more
    know_more = input("\n❓ Do you want to know more about this? (yes/no): ").strip().lower()
    if know_more == "yes":
        open_wikipedia_page(search_term, lang)

    # Ask if the user wants to export to PDF
    export_pdf = input("\n❓ Do you want to export this information to a PDF? (yes/no): ").strip().lower()
    if export_pdf == "yes":
        export_to_pdf(search_term, wikipedia_summary, image)

def main():
    search_history = []
    current_language = "en"  # Default language is English

    console.print(Panel.fit(Text("🌍 General Information Fetcher 🌍", style="bold blue")))
    console.print("\n📜 Instructions:-\n")
    console.print("1. Enter the name of any topic you want to search and learn about.")
    console.print("2. Type 'exit' or 'quit' to end the program.")
    console.print("3. If you want to know more about the topic, it will take you to Wikipedia.")
    console.print("4. You can change the language of the Wikipedia summary.")
    console.print("5. You can export the summary and image to a PDF.")
    console.print("6. Type 'languages' to view supported languages and their codes.")

    while True:
        search_term = input("\n🔍 Enter the Topic or Content (or 'menu' for options): ").strip()
        if search_term.lower() in ["exit", "quit"]:
            console.print("\n👋 Exiting the program. Goodbye!\n", style="bold blue")
            break
        elif search_term.lower() == "menu":
            console.print("\n📋 Menu:-\n")
            console.print("1. Search History")
            console.print("2. Change Language")
            console.print("3. Clear Cache")
            console.print("4. View Supported Languages")
            choice = input("\nEnter your choice: ").strip()
            if choice == "1":
                console.print("\n📜 Search History:")
                for idx, term in enumerate(search_history, 1):
                    console.print(f"{idx}. {term}")
            elif choice == "2":
                lang = input("Enter the language code (e.g., 'en' for English, 'es' for Spanish): ").strip()
                if lang in LANGUAGE_DESCRIPTIONS:
                    current_language = lang
                    console.print(f"🌐 Language set to {LANGUAGE_DESCRIPTIONS[lang]['name']} (Code: {lang}).", style="bold green")
                else:
                    console.print("⚠️ Invalid language code.", style="bold red")
            elif choice == "3":
                cache.clear()
                console.print("🧹 Cache cleared.", style="bold green")
            elif choice == "4":
                display_language_descriptions()
            else:
                console.print("⚠️ Invalid choice.", style="bold red")
        elif search_term.lower() == "languages":
            display_language_descriptions()
        elif search_term:
            search_history.append(search_term)
            display_info(search_term, current_language)
        else:
            console.print("\n⚠️ Please enter a valid name of the topic you want to search. ⚠️\n", style="bold red")

if __name__ == "__main__":
    main()