"""
SEO & Metadata Generator
Automates creation of titles, descriptions, tags, and chapters
"""

import logging
from colorama import Fore, Style

logger = logging.getLogger(__name__)

class MetadataGenerator:
    """
    Generates optimized video metadata for SEO
    """
    
    def __init__(self):
        """
        Initialize metadata generator
        """
        self.brand_name = "Living AuDHD"
        self.channel_focus = "ADHD productivity, AI automation, neurodivergent systems"
    
    def generate_description(self, title, topic, keywords, video_url=None):
        """
        Generate optimized YouTube description
        
        Args:
            title: Video title
            topic: Main topic/focus
            keywords: List of SEO keywords
            video_url: Link to video on channel
        
        Returns:
            Formatted description string
        """
        description = f"""{title}

In this video, we explore {topic}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 KEY TOPICS:
• {keywords[0] if keywords else 'Key insight 1'}
• {keywords[1] if len(keywords) > 1 else 'Key insight 2'}
• {keywords[2] if len(keywords) > 2 else 'Key insight 3'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 RESOURCES & LINKS:

📧 Join the Living AuDHD Community:
https://www.youtube.com/@livingaudhd

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 TIMESTAMPS:
0:00 - Introduction

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 ABOUT THIS CHANNEL:
{self.brand_name} is dedicated to helping neurodivergent individuals, particularly those with ADHD and autism, build sustainable productivity systems, harness AI automation, and create operating systems for their lives.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Keywords: {', '.join(keywords) if keywords else 'ADHD, productivity, AI'}
"""
        
        print(f"{Fore.GREEN}✓ Description generated{Style.RESET_ALL}")
        logger.info("Description generated")
        return description
    
    def generate_tags(self, title, topic, keywords, max_tags=30):
        """
        Generate optimized tags for video
        
        Args:
            title: Video title
            topic: Main topic
            keywords: List of SEO keywords
            max_tags: Maximum number of tags
        
        Returns:
            List of tags
        """
        # Core tags
        tags = [
            "ADHD",
            "Productivity",
            "Neurodivergent",
            "AI Automation",
            "Life Systems",
            self.brand_name,
        ]
        
        # Add provided keywords
        if keywords:
            for keyword in keywords[:10]:
                if keyword and keyword not in tags:
                    tags.append(keyword)
        
        # Add topic-related tags
        topic_tags = [
            f"{topic} ADHD",
            f"ADHD {topic}",
            f"{topic} productivity",
        ]
        
        tags.extend([t for t in topic_tags if t not in tags])
        
        # Limit to max tags
        tags = tags[:max_tags]
        
        print(f"{Fore.GREEN}✓ Generated {len(tags)} tags{Style.RESET_ALL}")
        logger.info(f"Generated {len(tags)} tags")
        return tags
    
    def generate_chapters(self, transcript_with_times):
        """
        Generate chapter markers from transcript
        
        Args:
            transcript_with_times: List of dicts with 'time' and 'text'
        
        Returns:
            Formatted chapters string
        """
        chapters = "0:00 Introduction\n"
        
        # Simple chapter generation from key phrases
        chapter_keywords = [
            "First", "Second", "Third",
            "Let", "So", "Now",
            "Today", "Important", "Remember"
        ]
        
        for item in transcript_with_times[:5]:
            time = item.get('time', '0:00')
            text = item.get('text', '')[:50]
            chapters += f"{time} - {text}\n"
        
        print(f"{Fore.GREEN}✓ Chapters generated{Style.RESET_ALL}")
        logger.info("Chapters generated")
        return chapters
    
    def optimize_title(self, topic, max_length=60):
        """
        Generate optimized title with hooks
        
        Args:
            topic: Main topic
            max_length: Maximum title length
        
        Returns:
            Optimized title
        """
        hooks = [
            f"How to {topic} with ADHD",
            f"The {topic} System That Changed My Life",
            f"Why {topic} Matters (ADHD Edition)",
            f"{topic}: The Complete Guide",
            f"Stop Struggling with {topic} - Do This Instead",
        ]
        
        # Use first hook that fits
        for title in hooks:
            if len(title) <= max_length:
                print(f"{Fore.GREEN}✓ Title optimized: {title}{Style.RESET_ALL}")
                logger.info(f"Title: {title}")
                return title
        
        # Fallback
        fallback = f"{topic} for ADHD"
        print(f"{Fore.YELLOW}⚠ Using fallback title: {fallback}{Style.RESET_ALL}")
        return fallback
