# Advanced-Multilingual-Knowledge-Retrieval-System
Advanced Multilingual Knowledge Retrieval System is a project that allows users to retrieve summarized information and images from Wikipedia using the Wikipedia REST API. This interactive command-line application supports multilingual searches, displays images, provides Wikipedia page links, and enables exporting summaries to PDF format also.

Designed with performance optimization in mind, the tool leverages API caching to reduce redundant requests, ensuring a seamless user experience.

🚀 Features
✅ Retrieve Wikipedia summaries using the Wikipedia REST API
✅ Fetch and display images from Wikipedia dynamically
✅ Open Wikipedia pages directly from the command line
✅ Export retrieved information and images to a PDF
✅ Multi-language support with descriptions for different scripts
✅ User-friendly CLI interface powered by the rich library
✅ Built-in API response caching for optimized performance

🔧 Technology Stack
APIs Used:
Wikipedia REST API – for fetching summaries
Wikipedia Media API – for retrieving images
Libraries & Frameworks:
requests – API requests and data fetching
PIL (Pillow) – Image processing and display
webbrowser – Wikipedia page redirection
rich – Interactive and formatted console output
fpdf – PDF generation for exporting information
🛠 Installation & Setup
Clone the repository:
sh
Copy
Edit
git clone https://github.com/yourusername/GeneralInfoFetcher.git
cd GeneralInfoFetcher
Install dependencies:
sh
Copy
Edit
pip install -r requirements.txt
Run the application:
sh
Copy
Edit
python PowerQuery.py
🎯 Usage Guide
Enter a topic to fetch information from Wikipedia.
Choose from the following options:
View Wikipedia summary
Display images (if available)
Open the full Wikipedia page in a web browser
Export the summary and image to a PDF
🔄 Supported Languages
This project supports multiple languages for Wikipedia searches, including:

English (en)
Spanish (es)
Chinese (zh)
Hindi (hi)
Arabic (ar)
French (fr)
Japanese (ja)
Russian (ru)
📜 API Implementation Details
The project interacts with Wikipedia’s API to fetch real-time information. The following API endpoints are utilized:

🔹 Fetching Wikipedia Summary
Endpoint:
ruby
Copy
Edit
https://{lang}.wikipedia.org/api/rest_v1/page/summary/{search_term}
Example Usage in Python:
python
Copy
Edit
response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_term}")
summary = response.json().get("extract", "No summary available.")
🔹 Fetching Wikipedia Images
Endpoint:
perl
Copy
Edit
https://{lang}.wikipedia.org/w/api.php?action=query&titles={search_term}&prop=pageimages&format=json&pithumbsize=500
Example Usage in Python:
python
Copy
Edit
response = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&titles={search_term}&prop=pageimages&format=json&pithumbsize=500")
image_url = response.json().get("query", {}).get("pages", {}).values()
🏆 Key Benefits of This Project
✔ Real-time Wikipedia data retrieval
✔ Cross-language Wikipedia search support
✔ Lightweight and efficient API request handling
✔ User-friendly CLI with rich text formatting
✔ Data export to PDF for offline use
