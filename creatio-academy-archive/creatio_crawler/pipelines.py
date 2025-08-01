# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import hashlib
from urllib.parse import urljoin, urlparse
from itemadapter import ItemAdapter
from creatio_crawler.items import PageItem, ResourceItem


class CreatioCrawlerPipeline:
    """Basic pipeline for data validation and processing"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Validate required fields
        if not adapter.get('url'):
            spider.logger.warning(f"Item missing URL: {item}")
            return item
            
        return item


class HTMLSavingPipeline:
    """Pipeline for saving raw HTML content to files"""
    
    def __init__(self):
        self.pages_dir = 'pages/raw'
        os.makedirs(self.pages_dir, exist_ok=True)
    
    def process_item(self, item, spider):
        if isinstance(item, PageItem):
            adapter = ItemAdapter(item)
            url = adapter.get('url')
            html_content = adapter.get('html_content')
            
            if url and html_content:
                # Create filename based on URL hash
                url_hash = hashlib.md5(url.encode()).hexdigest()
                filename = f"{url_hash}.html"
                filepath = os.path.join(self.pages_dir, filename)
                
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    spider.logger.info(f"Saved HTML for {url} to {filepath}")
                except Exception as e:
                    spider.logger.error(f"Failed to save HTML for {url}: {e}")
        
        return item


class SitemapPipeline:
    """Pipeline for building and maintaining comprehensive sitemap"""
    
    def __init__(self):
        self.sitemap_data = {
            'html_pages': [],
            'videos': {
                'youtube': [],
                'vimeo': [],
                'direct': []
            },
            'pdfs': [],
            'images': [],
            'other_resources': []
        }
        self.sitemap_file = 'sitemap.json'
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if isinstance(item, PageItem):
            url = adapter.get('url')
            title = adapter.get('title', '')
            content_type = adapter.get('content_type', '')
            
            page_data = {
                'url': url,
                'title': title,
                'content_type': content_type,
                'timestamp': adapter.get('crawl_timestamp'),
                'depth': adapter.get('depth', 0)
            }
            
            self.sitemap_data['html_pages'].append(page_data)
            
            # Process media links found on the page
            media_links = adapter.get('media_links', [])
            for media_url, media_type in media_links:
                self._categorize_media(media_url, media_type, url)
        
        elif isinstance(item, ResourceItem):
            url = adapter.get('url')
            resource_type = adapter.get('resource_type', '')
            
            resource_data = {
                'url': url,
                'resource_type': resource_type,
                'content_type': adapter.get('content_type', ''),
                'parent_page': adapter.get('parent_page'),
                'timestamp': adapter.get('crawl_timestamp')
            }
            
            self._categorize_resource(resource_data, resource_type)
        
        return item
    
    def _categorize_media(self, url, media_type, parent_url):
        """Categorize media links found on pages"""
        media_data = {
            'url': url,
            'parent_page': parent_url,
            'media_type': media_type
        }
        
        if 'youtube.com' in url or 'youtu.be' in url:
            self.sitemap_data['videos']['youtube'].append(media_data)
        elif 'vimeo.com' in url:
            self.sitemap_data['videos']['vimeo'].append(media_data)
        elif media_type.startswith('video/'):
            self.sitemap_data['videos']['direct'].append(media_data)
        elif media_type == 'application/pdf':
            self.sitemap_data['pdfs'].append(media_data)
        elif media_type.startswith('image/'):
            self.sitemap_data['images'].append(media_data)
        else:
            self.sitemap_data['other_resources'].append(media_data)
    
    def _categorize_resource(self, resource_data, resource_type):
        """Categorize discovered resources"""
        url = resource_data['url']
        
        if resource_type == 'pdf' or url.endswith('.pdf'):
            self.sitemap_data['pdfs'].append(resource_data)
        elif resource_type == 'image' or any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']):
            self.sitemap_data['images'].append(resource_data)
        elif resource_type == 'video' or any(url.endswith(ext) for ext in ['.mp4', '.webm', '.ogg', '.avi', '.mov']):
            self.sitemap_data['videos']['direct'].append(resource_data)
        else:
            self.sitemap_data['other_resources'].append(resource_data)
    
    def close_spider(self, spider):
        """Save sitemap data to JSON file when spider closes"""
        try:
            # Add summary statistics
            self.sitemap_data['summary'] = {
                'total_pages': len(self.sitemap_data['html_pages']),
                'total_youtube_videos': len(self.sitemap_data['videos']['youtube']),
                'total_vimeo_videos': len(self.sitemap_data['videos']['vimeo']),
                'total_direct_videos': len(self.sitemap_data['videos']['direct']),
                'total_pdfs': len(self.sitemap_data['pdfs']),
                'total_images': len(self.sitemap_data['images']),
                'total_other_resources': len(self.sitemap_data['other_resources'])
            }
            
            with open(self.sitemap_file, 'w', encoding='utf-8') as f:
                json.dump(self.sitemap_data, f, indent=2, ensure_ascii=False)
            
            spider.logger.info(f"Sitemap saved to {self.sitemap_file}")
            spider.logger.info(f"Summary: {self.sitemap_data['summary']}")
        except Exception as e:
            spider.logger.error(f"Failed to save sitemap: {e}")
