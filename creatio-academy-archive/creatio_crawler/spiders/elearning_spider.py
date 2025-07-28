import scrapy
import re
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from creatio_crawler.items import PageItem, ResourceItem


class ElearningSpider(scrapy.Spider):
    name = 'elearning'
    allowed_domains = ['academy.creatio.com']
    start_urls = ['https://academy.creatio.com/e-learning']
    
    # Custom settings for this spider
    custom_settings = {
        'DEPTH_LIMIT': 10,
        'CLOSESPIDER_PAGECOUNT': 1000,  # Prevent infinite crawling
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_urls = set()
        self.media_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico'],
            'videos': ['.mp4', '.webm', '.ogg', '.avi', '.mov', '.m4v'],
            'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
            'other': ['.zip', '.rar', '.tar', '.gz', '.css', '.js', '.json', '.xml']
        }
    
    def parse(self, response):
        """Main parsing method for the e-learning pages"""
        current_url = response.url
        
        # Avoid duplicate processing
        if current_url in self.visited_urls:
            return
        self.visited_urls.add(current_url)
        
        self.logger.info(f'Parsing page: {current_url}')
        
        # Create PageItem
        page_item = PageItem()
        page_item['url'] = current_url
        page_item['title'] = self._extract_title(response)
        page_item['content_type'] = response.headers.get('Content-Type', b'').decode()
        page_item['status_code'] = response.status
        page_item['html_content'] = response.text
        page_item['text_content'] = self._extract_text_content(response)
        page_item['crawl_timestamp'] = datetime.now().isoformat()
        page_item['depth'] = response.meta.get('depth', 0)
        page_item['parent_url'] = response.meta.get('parent_url', '')
        
        # Extract all links and media
        links, media_links, resources = self._extract_links_and_media(response)
        page_item['links'] = links
        page_item['media_links'] = media_links
        page_item['resources'] = resources
        
        yield page_item
        
        # Follow internal links recursively
        for link_url in links:
            if self._is_valid_link(link_url):
                yield response.follow(
                    link_url, 
                    callback=self.parse,
                    meta={'parent_url': current_url}
                )
        
        # Process discovered resources
        for resource_url, resource_type in resources:
            if self._should_fetch_resource(resource_url, resource_type):
                yield response.follow(
                    resource_url,
                    callback=self.parse_resource,
                    meta={
                        'resource_type': resource_type,
                        'parent_page': current_url
                    }
                )
    
    def parse_resource(self, response):
        """Parse non-HTML resources (PDFs, images, etc.)"""
        resource_item = ResourceItem()
        resource_item['url'] = response.url
        resource_item['resource_type'] = response.meta.get('resource_type', 'unknown')
        resource_item['content_type'] = response.headers.get('Content-Type', b'').decode()
        resource_item['file_size'] = len(response.body) if response.body else 0
        resource_item['status_code'] = response.status
        resource_item['parent_page'] = response.meta.get('parent_page', '')
        resource_item['crawl_timestamp'] = datetime.now().isoformat()
        
        yield resource_item
    
    def _extract_title(self, response):
        """Extract page title"""
        title = response.css('title::text').get()
        if not title:
            title = response.css('h1::text').get()
        return title.strip() if title else 'No Title'
    
    def _extract_text_content(self, response):
        """Extract readable text content from HTML"""
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit text length
        except Exception as e:
            self.logger.error(f"Error extracting text content from {response.url}: {e}")
            return ""
    
    def _extract_links_and_media(self, response):
        """Extract all links, media links, and resources from the page"""
        links = []
        media_links = []
        resources = []
        
        # Extract all links
        all_links = response.css('a::attr(href)').getall()
        for link in all_links:
            absolute_link = urljoin(response.url, link)
            links.append(absolute_link)
        
        # Extract media elements
        # Images
        img_srcs = response.css('img::attr(src)').getall()
        for src in img_srcs:
            absolute_src = urljoin(response.url, src)
            media_links.append((absolute_src, 'image'))
            resources.append((absolute_src, 'image'))
        
        # Videos
        video_srcs = response.css('video source::attr(src)').getall()
        for src in video_srcs:
            absolute_src = urljoin(response.url, src)
            media_links.append((absolute_src, 'video'))
            resources.append((absolute_src, 'video'))
        
        # YouTube videos
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in youtube_patterns:
            matches = re.findall(pattern, response.text)
            for match in matches:
                youtube_url = f"https://www.youtube.com/watch?v={match}"
                media_links.append((youtube_url, 'youtube'))
        
        # Vimeo videos
        vimeo_pattern = r'(?:https?://)?(?:www\.)?vimeo\.com/(\d+)'
        vimeo_matches = re.findall(vimeo_pattern, response.text)
        for match in vimeo_matches:
            vimeo_url = f"https://vimeo.com/{match}"
            media_links.append((vimeo_url, 'vimeo'))
        
        # iframes (might contain videos)
        iframe_srcs = response.css('iframe::attr(src)').getall()
        for src in iframe_srcs:
            absolute_src = urljoin(response.url, src)
            if 'youtube.com' in src or 'youtu.be' in src:
                media_links.append((absolute_src, 'youtube'))
            elif 'vimeo.com' in src:
                media_links.append((absolute_src, 'vimeo'))
            else:
                media_links.append((absolute_src, 'iframe'))
        
        # Documents and other resources by examining all href attributes
        all_hrefs = response.css('a::attr(href)').getall()
        for href in all_hrefs:
            absolute_href = urljoin(response.url, href)
            resource_type = self._determine_resource_type(absolute_href)
            if resource_type != 'html':
                resources.append((absolute_href, resource_type))
        
        return links, media_links, resources
    
    def _determine_resource_type(self, url):
        """Determine resource type based on URL or extension"""
        parsed_url = urlparse(url.lower())
        path = parsed_url.path
        
        for resource_type, extensions in self.media_extensions.items():
            for ext in extensions:
                if path.endswith(ext):
                    return resource_type.rstrip('s')  # Return singular form
        
        return 'html'  # Default to HTML
    
    def _is_valid_link(self, url):
        """Check if a link should be followed"""
        parsed = urlparse(url)
        
        # Only follow links within the allowed domain
        if parsed.netloc and parsed.netloc not in self.allowed_domains:
            return False
        
        # Skip non-HTTP links
        if parsed.scheme and parsed.scheme not in ['http', 'https']:
            return False
        
        # Skip duplicate URLs
        if url in self.visited_urls:
            return False
        
        # Skip certain file types
        skip_extensions = ['.css', '.js', '.ico', '.zip', '.tar', '.gz']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False
        
        return True
    
    def _should_fetch_resource(self, url, resource_type):
        """Determine if we should fetch a resource"""
        # Only fetch PDFs and images for now
        return resource_type in ['pdf', 'image']
