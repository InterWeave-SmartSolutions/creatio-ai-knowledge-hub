import os
import requests
from bs4 import BeautifulSoup

# Create a directory to store the scraped data
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to download PDF materials
def download_pdf(url, path):
    try:
        response = requests.get(url)
        if response.headers['Content-Type'] == 'application/pdf':
            with open(path, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print(f"Error downloading PDF: {e}")

# Function to scrape course details
def scrape_course(course_url, save_dir):
    response = requests.get(course_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract descriptions, prerequisites, etc.
    description = soup.find('meta', {'name': 'description'})['content']
    # Assume existence of prerequisites and objectives sections, need to adjust if not structured this way
    prerequisites = soup.find(text='Prerequisites').find_next('ul').get_text(separator='; ')
    objectives = soup.find(text='Learning Objectives').find_next('ul').get_text(separator='; ')

    # Extract PDF and video links
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    video_links = [iframe['src'] for iframe in soup.find_all('iframe') if 'youtube' in iframe['src']]

    # Save the extracted data
    data_file = os.path.join(save_dir, 'course_info.txt')
    with open(data_file, 'w', encoding='utf-8') as f:
        f.write(f"Description: {description}\n")
        f.write(f"Prerequisites: {prerequisites}\n")
        f.write(f"Objectives: {objectives}\n")
        f.write("Video URLs:\n" + "\n".join(video_links) + "\n")

    # Download PDFs
    for pdf in pdf_links:
        pdf_file_name = pdf.split('/')[-1]
        download_pdf(pdf, os.path.join(save_dir, pdf_file_name))

# Main execution

course_data = [
    {
        "title": "Development on Creatio platform",
        "url": "https://academy.creatio.com/training/development-creatio-platform-5"
    },
    {
        "title": "Creatio administration and configuration (AUS)",
        "url": "https://academy.creatio.com/training/creatio-administration-and-configuration-aus"
    }
    # Add more courses here
]

base_dir = './scraped_courses'
create_directory(base_dir)

for course in course_data:
    course_dir = os.path.join(base_dir, course['title'].replace(' ', '_'))
    create_directory(course_dir)
    scrape_course(course['url'], course_dir)
