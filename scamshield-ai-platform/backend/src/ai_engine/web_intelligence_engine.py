"""
ScamShield AI - Web Intelligence Engine

Advanced web scraping, automation, and intelligence gathering for fraud investigation.
Includes stealth browsing, CAPTCHA solving, and intelligent data extraction.
"""

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import playwright
from playwright.async_api import async_playwright
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import json
import re
import time
import random
import hashlib
import base64
from urllib.parse import urljoin, urlparse, parse_qs
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import cv2
import numpy as np
from PIL import Image
import io
import dns.resolver
import whois
import ssl
import socket
from datetime import datetime, timezone
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..utils.error_handler import ErrorContext, APIError
from ..utils.logging_config import get_logger
from .ocr_engine import AdvancedOCREngine

logger = get_logger(__name__)


class BrowserType(Enum):
    """Supported browser types"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    PLAYWRIGHT = "playwright"
    REQUESTS = "requests"


class StealthLevel(Enum):
    """Stealth levels for browsing"""
    BASIC = "basic"
    MODERATE = "moderate"
    ADVANCED = "advanced"
    MAXIMUM = "maximum"


class CaptchaType(Enum):
    """Types of CAPTCHAs that can be solved"""
    RECAPTCHA_V2 = "recaptcha_v2"
    RECAPTCHA_V3 = "recaptcha_v3"
    HCAPTCHA = "hcaptcha"
    IMAGE_CAPTCHA = "image_captcha"
    TEXT_CAPTCHA = "text_captcha"


@dataclass
class WebPage:
    """Represents a scraped web page"""
    url: str
    title: str
    content: str
    html: str
    metadata: Dict[str, Any]
    links: List[str]
    images: List[str]
    forms: List[Dict[str, Any]]
    scripts: List[str]
    stylesheets: List[str]
    status_code: int
    response_time: float
    headers: Dict[str, str]
    cookies: Dict[str, str]
    screenshot: Optional[bytes]
    timestamp: datetime


@dataclass
class DomainIntelligence:
    """Domain intelligence data"""
    domain: str
    ip_address: str
    registrar: str
    registration_date: Optional[datetime]
    expiration_date: Optional[datetime]
    name_servers: List[str]
    mx_records: List[str]
    ssl_info: Dict[str, Any]
    reputation_score: float
    blacklist_status: Dict[str, bool]
    geolocation: Dict[str, Any]
    hosting_provider: str
    risk_indicators: List[str]


@dataclass
class SocialMediaProfile:
    """Social media profile information"""
    platform: str
    username: str
    display_name: str
    bio: str
    follower_count: int
    following_count: int
    post_count: int
    verified: bool
    profile_image: str
    recent_posts: List[Dict[str, Any]]
    account_age: Optional[datetime]
    suspicious_indicators: List[str]


class StealthBrowser:
    """Advanced stealth browser with anti-detection measures"""
    
    def __init__(self, browser_type: BrowserType = BrowserType.PLAYWRIGHT, stealth_level: StealthLevel = StealthLevel.ADVANCED):
        self.browser_type = browser_type
        self.stealth_level = stealth_level
        self.driver = None
        self.session = None
        self.playwright_browser = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
    
    async def initialize(self):
        """Initialize the browser with stealth settings"""
        with ErrorContext("browser_initialization"):
            if self.browser_type == BrowserType.CHROME:
                await self._init_chrome()
            elif self.browser_type == BrowserType.FIREFOX:
                await self._init_firefox()
            elif self.browser_type == BrowserType.PLAYWRIGHT:
                await self._init_playwright()
            elif self.browser_type == BrowserType.REQUESTS:
                await self._init_requests()
    
    async def _init_chrome(self):
        """Initialize Chrome with stealth settings"""
        options = uc.ChromeOptions()
        
        # Basic stealth options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        if self.stealth_level in [StealthLevel.ADVANCED, StealthLevel.MAXIMUM]:
            # Advanced stealth options
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-background-timer-throttling")
            
            # Random user agent
            user_agent = random.choice(self.user_agents)
            options.add_argument(f"--user-agent={user_agent}")
            
            # Random window size
            width = random.randint(1200, 1920)
            height = random.randint(800, 1080)
            options.add_argument(f"--window-size={width},{height}")
            
            if self.stealth_level == StealthLevel.MAXIMUM:
                # Maximum stealth - use residential proxy rotation
                # This would require a proxy service integration
                pass
        
        self.driver = uc.Chrome(options=options)
        
        # Execute stealth scripts
        await self._execute_stealth_scripts()
    
    async def _init_firefox(self):
        """Initialize Firefox with stealth settings"""
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from selenium.webdriver.firefox.service import Service
        
        options = FirefoxOptions()
        options.add_argument("--headless") if self.stealth_level == StealthLevel.MAXIMUM else None
        
        # Firefox-specific stealth settings
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", random.choice(self.user_agents))
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.set_preference("dom.webnotifications.enabled", False)
        profile.set_preference("media.navigator.enabled", False)
        
        self.driver = webdriver.Firefox(firefox_profile=profile, options=options)
        
        # Execute stealth scripts
        await self._execute_stealth_scripts()
    
    async def _init_playwright(self):
        """Initialize Playwright with stealth settings"""
        playwright_instance = await async_playwright().start()
        
        launch_options = {
            "headless": self.stealth_level == StealthLevel.MAXIMUM,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox"
            ]
        }
        
        if self.stealth_level in [StealthLevel.ADVANCED, StealthLevel.MAXIMUM]:
            # Advanced stealth for Playwright
            launch_options["args"].extend([
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--disable-ipc-flooding-protection"
            ])
        
        self.playwright_browser = await playwright_instance.chromium.launch(**launch_options)
        
        # Create context with stealth settings
        context_options = {
            "user_agent": random.choice(self.user_agents),
            "viewport": {
                "width": random.randint(1200, 1920),
                "height": random.randint(800, 1080)
            },
            "locale": "en-US",
            "timezone_id": "America/New_York"
        }
        
        self.context = await self.playwright_browser.new_context(**context_options)
        
        # Add stealth scripts
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
    
    async def _init_requests(self):
        """Initialize requests session with stealth settings"""
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": random.choice(self.user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            },
            timeout=aiohttp.ClientTimeout(total=30)
        )
    
    async def _execute_stealth_scripts(self):
        """Execute JavaScript to hide automation"""
        if self.driver:
            stealth_js = """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                
                window.chrome = {
                    runtime: {},
                };
                
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Hide selenium indicators
                delete window.selenium;
                delete window._selenium;
                delete window.__selenium_unwrapped;
                delete window.__selenium_evaluate;
                delete window.__webdriver_evaluate;
                delete window.__driver_evaluate;
                delete window.__webdriver_unwrapped;
                delete window.__driver_unwrapped;
                delete window._Selenium_IDE_Recorder;
                delete window.__webdriverFunc;
                delete window.domAutomation;
                delete window.domAutomationController;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """
            
            self.driver.execute_script(stealth_js)
    
    async def navigate(self, url: str) -> WebPage:
        """Navigate to URL and return page data"""
        with ErrorContext("page_navigation", url=url):
            start_time = time.time()
            
            if self.browser_type == BrowserType.PLAYWRIGHT:
                return await self._navigate_playwright(url, start_time)
            elif self.browser_type == BrowserType.REQUESTS:
                return await self._navigate_requests(url, start_time)
            else:
                return await self._navigate_selenium(url, start_time)
    
    async def _navigate_playwright(self, url: str, start_time: float) -> WebPage:
        """Navigate using Playwright"""
        page = await self.context.new_page()
        
        try:
            response = await page.goto(url, wait_until="networkidle")
            
            # Wait for page to load
            await page.wait_for_load_state("domcontentloaded")
            
            # Extract page data
            title = await page.title()
            content = await page.inner_text("body")
            html = await page.content()
            
            # Extract links
            links = await page.evaluate("""
                () => Array.from(document.links).map(link => link.href)
            """)
            
            # Extract images
            images = await page.evaluate("""
                () => Array.from(document.images).map(img => img.src)
            """)
            
            # Extract forms
            forms = await page.evaluate("""
                () => Array.from(document.forms).map(form => ({
                    action: form.action,
                    method: form.method,
                    fields: Array.from(form.elements).map(el => ({
                        name: el.name,
                        type: el.type,
                        required: el.required
                    }))
                }))
            """)
            
            # Take screenshot
            screenshot = await page.screenshot(full_page=True)
            
            response_time = time.time() - start_time
            
            return WebPage(
                url=url,
                title=title,
                content=content,
                html=html,
                metadata={"user_agent": self.user_agents[0]},
                links=links,
                images=images,
                forms=forms,
                scripts=[],
                stylesheets=[],
                status_code=response.status,
                response_time=response_time,
                headers=dict(response.headers),
                cookies={},
                screenshot=screenshot,
                timestamp=datetime.now(timezone.utc)
            )
        
        finally:
            await page.close()
    
    async def _navigate_requests(self, url: str, start_time: float) -> WebPage:
        """Navigate using aiohttp requests"""
        async with self.session.get(url) as response:
            html = await response.text()
            headers = dict(response.headers)
            status_code = response.status
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            title = soup.title.string if soup.title else ""
            content = soup.get_text()
            
            # Extract links
            links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]
            
            # Extract images
            images = [urljoin(url, img.get('src')) for img in soup.find_all('img', src=True)]
            
            # Extract forms
            forms = []
            for form in soup.find_all('form'):
                form_data = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'get'),
                    'fields': []
                }
                
                for input_field in form.find_all(['input', 'select', 'textarea']):
                    form_data['fields'].append({
                        'name': input_field.get('name', ''),
                        'type': input_field.get('type', ''),
                        'required': input_field.has_attr('required')
                    })
                
                forms.append(form_data)
            
            response_time = time.time() - start_time
            
            return WebPage(
                url=url,
                title=title,
                content=content,
                html=html,
                metadata={},
                links=links,
                images=images,
                forms=forms,
                scripts=[],
                stylesheets=[],
                status_code=status_code,
                response_time=response_time,
                headers=headers,
                cookies={},
                screenshot=None,
                timestamp=datetime.now(timezone.utc)
            )
    
    async def _navigate_selenium(self, url: str, start_time: float) -> WebPage:
        """Navigate using Selenium"""
        self.driver.get(url)
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Extract page data
        title = self.driver.title
        content = self.driver.find_element(By.TAG_NAME, "body").text
        html = self.driver.page_source
        
        # Extract links
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")
        links = [link.get_attribute("href") for link in link_elements if link.get_attribute("href")]
        
        # Extract images
        img_elements = self.driver.find_elements(By.TAG_NAME, "img")
        images = [img.get_attribute("src") for img in img_elements if img.get_attribute("src")]
        
        # Extract forms
        form_elements = self.driver.find_elements(By.TAG_NAME, "form")
        forms = []
        for form in form_elements:
            form_data = {
                'action': form.get_attribute("action") or '',
                'method': form.get_attribute("method") or 'get',
                'fields': []
            }
            
            inputs = form.find_elements(By.TAG_NAME, "input")
            for input_field in inputs:
                form_data['fields'].append({
                    'name': input_field.get_attribute("name") or '',
                    'type': input_field.get_attribute("type") or '',
                    'required': input_field.get_attribute("required") is not None
                })
            
            forms.append(form_data)
        
        # Take screenshot
        screenshot = self.driver.get_screenshot_as_png()
        
        response_time = time.time() - start_time
        
        return WebPage(
            url=url,
            title=title,
            content=content,
            html=html,
            metadata={},
            links=links,
            images=images,
            forms=forms,
            scripts=[],
            stylesheets=[],
            status_code=200,  # Selenium doesn't provide status code directly
            response_time=response_time,
            headers={},
            cookies={},
            screenshot=screenshot,
            timestamp=datetime.now(timezone.utc)
        )
    
    async def solve_captcha(self, captcha_type: CaptchaType, element_selector: str = None) -> bool:
        """Attempt to solve CAPTCHA"""
        with ErrorContext("captcha_solving"):
            try:
                if captcha_type == CaptchaType.IMAGE_CAPTCHA:
                    return await self._solve_image_captcha(element_selector)
                elif captcha_type == CaptchaType.TEXT_CAPTCHA:
                    return await self._solve_text_captcha(element_selector)
                else:
                    logger.warning(f"CAPTCHA type {captcha_type} not supported for automated solving")
                    return False
            except Exception as e:
                logger.error(f"CAPTCHA solving failed: {str(e)}")
                return False
    
    async def _solve_image_captcha(self, element_selector: str) -> bool:
        """Solve image-based CAPTCHA using OCR"""
        if self.browser_type == BrowserType.PLAYWRIGHT:
            page = await self.context.new_page()
            captcha_element = await page.query_selector(element_selector)
            if captcha_element:
                screenshot = await captcha_element.screenshot()
                
                # Use OCR to extract text
                ocr_engine = AdvancedOCREngine()
                result = await ocr_engine.extract_text(screenshot)
                
                # Find input field and enter text
                input_field = await page.query_selector("input[type='text']")
                if input_field:
                    await input_field.fill(result.text.strip())
                    return True
            
            await page.close()
        
        return False
    
    async def _solve_text_captcha(self, element_selector: str) -> bool:
        """Solve text-based CAPTCHA using AI"""
        # This would integrate with AI models to solve text-based CAPTCHAs
        # For now, return False as manual intervention is needed
        return False
    
    async def close(self):
        """Close browser and cleanup"""
        try:
            if self.driver:
                self.driver.quit()
            if self.session:
                await self.session.close()
            if self.playwright_browser:
                await self.playwright_browser.close()
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")


class DomainAnalyzer:
    """Advanced domain intelligence and analysis"""
    
    def __init__(self):
        self.reputation_apis = {
            "virustotal": "https://www.virustotal.com/vtapi/v2/domain/report",
            "urlvoid": "https://www.urlvoid.com/api1000",
            "safebrowsing": "https://safebrowsing.googleapis.com/v4/threatMatches:find"
        }
    
    async def analyze_domain(self, domain: str) -> DomainIntelligence:
        """Comprehensive domain analysis"""
        with ErrorContext("domain_analysis", domain=domain):
            # Run all analysis tasks in parallel
            tasks = [
                self._get_whois_info(domain),
                self._get_dns_info(domain),
                self._get_ssl_info(domain),
                self._check_reputation(domain),
                self._analyze_risk_indicators(domain)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine results
            whois_info = results[0] if not isinstance(results[0], Exception) else {}
            dns_info = results[1] if not isinstance(results[1], Exception) else {}
            ssl_info = results[2] if not isinstance(results[2], Exception) else {}
            reputation = results[3] if not isinstance(results[3], Exception) else {}
            risk_indicators = results[4] if not isinstance(results[4], Exception) else []
            
            # Calculate reputation score
            reputation_score = self._calculate_reputation_score(
                whois_info, dns_info, ssl_info, reputation, risk_indicators
            )
            
            return DomainIntelligence(
                domain=domain,
                ip_address=dns_info.get('ip_address', ''),
                registrar=whois_info.get('registrar', ''),
                registration_date=whois_info.get('creation_date'),
                expiration_date=whois_info.get('expiration_date'),
                name_servers=dns_info.get('name_servers', []),
                mx_records=dns_info.get('mx_records', []),
                ssl_info=ssl_info,
                reputation_score=reputation_score,
                blacklist_status=reputation.get('blacklists', {}),
                geolocation=dns_info.get('geolocation', {}),
                hosting_provider=dns_info.get('hosting_provider', ''),
                risk_indicators=risk_indicators
            )
    
    async def _get_whois_info(self, domain: str) -> Dict[str, Any]:
        """Get WHOIS information"""
        try:
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': w.creation_date,
                'expiration_date': w.expiration_date,
                'updated_date': w.updated_date,
                'status': w.status,
                'name_servers': w.name_servers,
                'emails': w.emails
            }
        except Exception as e:
            logger.warning(f"WHOIS lookup failed for {domain}: {str(e)}")
            return {}
    
    async def _get_dns_info(self, domain: str) -> Dict[str, Any]:
        """Get DNS information"""
        try:
            # Resolve IP address
            ip_address = socket.gethostbyname(domain)
            
            # Get name servers
            name_servers = []
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                name_servers = [str(record) for record in ns_records]
            except:
                pass
            
            # Get MX records
            mx_records = []
            try:
                mx_records_result = dns.resolver.resolve(domain, 'MX')
                mx_records = [str(record) for record in mx_records_result]
            except:
                pass
            
            return {
                'ip_address': ip_address,
                'name_servers': name_servers,
                'mx_records': mx_records,
                'geolocation': {},  # Would integrate with geolocation API
                'hosting_provider': ''  # Would integrate with hosting provider API
            }
        except Exception as e:
            logger.warning(f"DNS lookup failed for {domain}: {str(e)}")
            return {}
    
    async def _get_ssl_info(self, domain: str) -> Dict[str, Any]:
        """Get SSL certificate information"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'version': cert.get('version'),
                        'serial_number': cert.get('serialNumber'),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter'),
                        'signature_algorithm': cert.get('signatureAlgorithm')
                    }
        except Exception as e:
            logger.warning(f"SSL check failed for {domain}: {str(e)}")
            return {}
    
    async def _check_reputation(self, domain: str) -> Dict[str, Any]:
        """Check domain reputation against multiple blacklists"""
        reputation = {
            'blacklists': {},
            'threat_intelligence': {}
        }
        
        # This would integrate with various reputation APIs
        # For now, return empty results
        
        return reputation
    
    async def _analyze_risk_indicators(self, domain: str) -> List[str]:
        """Analyze domain for risk indicators"""
        risk_indicators = []
        
        # Check domain characteristics
        if len(domain) > 50:
            risk_indicators.append("unusually_long_domain")
        
        if domain.count('.') > 3:
            risk_indicators.append("multiple_subdomains")
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}',  # IP-like pattern
            r'[a-z]{10,}[0-9]+',  # Random string with numbers
            r'(bit\.ly|tinyurl|t\.co|goo\.gl)',  # URL shorteners
            r'(secure|verify|update|confirm)',  # Phishing keywords
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, domain, re.IGNORECASE):
                risk_indicators.append(f"suspicious_pattern_{pattern}")
        
        return risk_indicators
    
    def _calculate_reputation_score(
        self, 
        whois_info: Dict, 
        dns_info: Dict, 
        ssl_info: Dict, 
        reputation: Dict, 
        risk_indicators: List[str]
    ) -> float:
        """Calculate overall reputation score (0-1, higher is better)"""
        score = 1.0
        
        # Penalize for risk indicators
        score -= len(risk_indicators) * 0.1
        
        # Penalize for missing SSL
        if not ssl_info:
            score -= 0.2
        
        # Penalize for recent registration
        if whois_info.get('creation_date'):
            domain_age = (datetime.now() - whois_info['creation_date']).days
            if domain_age < 30:
                score -= 0.3
            elif domain_age < 90:
                score -= 0.1
        
        # Penalize for blacklist status
        blacklist_count = sum(1 for status in reputation.get('blacklists', {}).values() if status)
        score -= blacklist_count * 0.2
        
        return max(0.0, min(1.0, score))


class SocialMediaIntelligence:
    """Social media intelligence gathering"""
    
    def __init__(self):
        self.platforms = {
            'twitter': self._analyze_twitter,
            'linkedin': self._analyze_linkedin,
            'facebook': self._analyze_facebook,
            'instagram': self._analyze_instagram,
            'telegram': self._analyze_telegram
        }
    
    async def analyze_profile(self, platform: str, username: str) -> SocialMediaProfile:
        """Analyze social media profile"""
        with ErrorContext("social_media_analysis", platform=platform, username=username):
            if platform.lower() in self.platforms:
                return await self.platforms[platform.lower()](username)
            else:
                raise APIError(f"Platform {platform} not supported")
    
    async def _analyze_twitter(self, username: str) -> SocialMediaProfile:
        """Analyze Twitter profile"""
        # This would integrate with Twitter API or scraping
        # For now, return mock data structure
        return SocialMediaProfile(
            platform="twitter",
            username=username,
            display_name="",
            bio="",
            follower_count=0,
            following_count=0,
            post_count=0,
            verified=False,
            profile_image="",
            recent_posts=[],
            account_age=None,
            suspicious_indicators=[]
        )
    
    async def _analyze_linkedin(self, username: str) -> SocialMediaProfile:
        """Analyze LinkedIn profile"""
        # Implementation would go here
        return SocialMediaProfile(
            platform="linkedin",
            username=username,
            display_name="",
            bio="",
            follower_count=0,
            following_count=0,
            post_count=0,
            verified=False,
            profile_image="",
            recent_posts=[],
            account_age=None,
            suspicious_indicators=[]
        )
    
    async def _analyze_facebook(self, username: str) -> SocialMediaProfile:
        """Analyze Facebook profile"""
        # Implementation would go here
        return SocialMediaProfile(
            platform="facebook",
            username=username,
            display_name="",
            bio="",
            follower_count=0,
            following_count=0,
            post_count=0,
            verified=False,
            profile_image="",
            recent_posts=[],
            account_age=None,
            suspicious_indicators=[]
        )
    
    async def _analyze_instagram(self, username: str) -> SocialMediaProfile:
        """Analyze Instagram profile"""
        # Implementation would go here
        return SocialMediaProfile(
            platform="instagram",
            username=username,
            display_name="",
            bio="",
            follower_count=0,
            following_count=0,
            post_count=0,
            verified=False,
            profile_image="",
            recent_posts=[],
            account_age=None,
            suspicious_indicators=[]
        )
    
    async def _analyze_telegram(self, username: str) -> SocialMediaProfile:
        """Analyze Telegram profile"""
        # Implementation would go here
        return SocialMediaProfile(
            platform="telegram",
            username=username,
            display_name="",
            bio="",
            follower_count=0,
            following_count=0,
            post_count=0,
            verified=False,
            profile_image="",
            recent_posts=[],
            account_age=None,
            suspicious_indicators=[]
        )


class WebIntelligenceEngine:
    """Main web intelligence engine orchestrating all components"""
    
    def __init__(self):
        self.browser = None
        self.domain_analyzer = DomainAnalyzer()
        self.social_media = SocialMediaIntelligence()
        self.ocr_engine = AdvancedOCREngine()
    
    async def initialize(
        self, 
        browser_type: BrowserType = BrowserType.PLAYWRIGHT,
        stealth_level: StealthLevel = StealthLevel.ADVANCED
    ):
        """Initialize the web intelligence engine"""
        self.browser = StealthBrowser(browser_type, stealth_level)
        await self.browser.initialize()
    
    async def investigate_url(self, url: str) -> Dict[str, Any]:
        """Comprehensive URL investigation"""
        with ErrorContext("url_investigation", url=url):
            # Parse domain from URL
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # Run parallel investigations
            tasks = [
                self.browser.navigate(url),
                self.domain_analyzer.analyze_domain(domain),
                self._analyze_url_structure(url)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            webpage = results[0] if not isinstance(results[0], Exception) else None
            domain_intel = results[1] if not isinstance(results[1], Exception) else None
            url_analysis = results[2] if not isinstance(results[2], Exception) else {}
            
            # Analyze page content if available
            content_analysis = {}
            if webpage:
                content_analysis = await self._analyze_page_content(webpage)
            
            # Compile comprehensive report
            investigation_report = {
                'url': url,
                'domain': domain,
                'webpage': asdict(webpage) if webpage else None,
                'domain_intelligence': asdict(domain_intel) if domain_intel else None,
                'url_analysis': url_analysis,
                'content_analysis': content_analysis,
                'risk_assessment': self._assess_overall_risk(webpage, domain_intel, url_analysis, content_analysis),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
            return investigation_report
    
    async def _analyze_url_structure(self, url: str) -> Dict[str, Any]:
        """Analyze URL structure for suspicious patterns"""
        parsed = urlparse(url)
        
        analysis = {
            'scheme': parsed.scheme,
            'domain': parsed.netloc,
            'path': parsed.path,
            'query_params': parse_qs(parsed.query),
            'fragment': parsed.fragment,
            'suspicious_indicators': []
        }
        
        # Check for suspicious patterns
        if parsed.scheme != 'https':
            analysis['suspicious_indicators'].append('non_https')
        
        if len(parsed.netloc) > 50:
            analysis['suspicious_indicators'].append('long_domain')
        
        if re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', parsed.netloc):
            analysis['suspicious_indicators'].append('ip_address_domain')
        
        # Check for URL shorteners
        shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
        if any(shortener in parsed.netloc for shortener in shorteners):
            analysis['suspicious_indicators'].append('url_shortener')
        
        # Check for suspicious keywords
        suspicious_keywords = ['secure', 'verify', 'update', 'confirm', 'login', 'bank']
        url_lower = url.lower()
        for keyword in suspicious_keywords:
            if keyword in url_lower:
                analysis['suspicious_indicators'].append(f'suspicious_keyword_{keyword}')
        
        return analysis
    
    async def _analyze_page_content(self, webpage: WebPage) -> Dict[str, Any]:
        """Analyze webpage content for fraud indicators"""
        analysis = {
            'text_analysis': {},
            'form_analysis': {},
            'link_analysis': {},
            'image_analysis': {},
            'fraud_indicators': []
        }
        
        # Analyze text content
        text_analysis = self._analyze_text_content(webpage.content)
        analysis['text_analysis'] = text_analysis
        
        # Analyze forms for data collection
        form_analysis = self._analyze_forms(webpage.forms)
        analysis['form_analysis'] = form_analysis
        
        # Analyze links for suspicious destinations
        link_analysis = await self._analyze_links(webpage.links)
        analysis['link_analysis'] = link_analysis
        
        # Analyze images using OCR if screenshot available
        if webpage.screenshot:
            image_analysis = await self._analyze_screenshot(webpage.screenshot)
            analysis['image_analysis'] = image_analysis
        
        # Compile fraud indicators
        fraud_indicators = []
        fraud_indicators.extend(text_analysis.get('fraud_keywords', []))
        fraud_indicators.extend(form_analysis.get('suspicious_fields', []))
        fraud_indicators.extend(link_analysis.get('suspicious_links', []))
        
        analysis['fraud_indicators'] = fraud_indicators
        
        return analysis
    
    def _analyze_text_content(self, content: str) -> Dict[str, Any]:
        """Analyze text content for fraud indicators"""
        fraud_keywords = [
            'urgent', 'immediate', 'act now', 'limited time', 'expires today',
            'congratulations', 'winner', 'selected', 'claim now', 'free money',
            'guaranteed', 'risk-free', 'no questions asked', 'secret',
            'verify account', 'suspended', 'blocked', 'unauthorized access',
            'click here', 'download now', 'install now', 'update required'
        ]
        
        content_lower = content.lower()
        found_keywords = [kw for kw in fraud_keywords if kw in content_lower]
        
        # Count urgency indicators
        urgency_count = sum(1 for kw in ['urgent', 'immediate', 'expires', 'limited'] if kw in content_lower)
        
        # Check for money-related terms
        money_terms = ['$', 'money', 'cash', 'prize', 'reward', 'payment']
        money_mentions = sum(1 for term in money_terms if term in content_lower)
        
        return {
            'fraud_keywords': found_keywords,
            'urgency_score': urgency_count,
            'money_mentions': money_mentions,
            'total_text_length': len(content),
            'fraud_keyword_density': len(found_keywords) / max(1, len(content.split())) * 100
        }
    
    def _analyze_forms(self, forms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze forms for suspicious data collection"""
        analysis = {
            'total_forms': len(forms),
            'suspicious_fields': [],
            'sensitive_data_requested': []
        }
        
        sensitive_fields = [
            'password', 'ssn', 'social security', 'credit card', 'card number',
            'cvv', 'pin', 'bank account', 'routing number', 'social'
        ]
        
        for form in forms:
            for field in form.get('fields', []):
                field_name = field.get('name', '').lower()
                field_type = field.get('type', '').lower()
                
                # Check for sensitive data collection
                for sensitive in sensitive_fields:
                    if sensitive in field_name:
                        analysis['sensitive_data_requested'].append(sensitive)
                
                # Check for suspicious field patterns
                if field_type == 'password' and 'current' not in field_name:
                    analysis['suspicious_fields'].append('unexpected_password_field')
                
                if 'credit' in field_name or 'card' in field_name:
                    analysis['suspicious_fields'].append('credit_card_request')
        
        return analysis
    
    async def _analyze_links(self, links: List[str]) -> Dict[str, Any]:
        """Analyze links for suspicious destinations"""
        analysis = {
            'total_links': len(links),
            'external_links': [],
            'suspicious_links': [],
            'url_shorteners': []
        }
        
        shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
        
        for link in links:
            if link:
                parsed = urlparse(link)
                
                # Check for URL shorteners
                if any(shortener in parsed.netloc for shortener in shorteners):
                    analysis['url_shorteners'].append(link)
                    analysis['suspicious_links'].append(link)
                
                # Check for suspicious patterns
                if re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', parsed.netloc):
                    analysis['suspicious_links'].append(link)
        
        return analysis
    
    async def _analyze_screenshot(self, screenshot: bytes) -> Dict[str, Any]:
        """Analyze screenshot using OCR and image analysis"""
        try:
            # Convert screenshot to numpy array
            nparr = np.frombuffer(screenshot, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Extract text using OCR
            ocr_result = await self.ocr_engine.extract_text(img)
            
            # Analyze extracted text for fraud indicators
            fraud_analysis = self.ocr_engine.extract_specific_patterns(ocr_result.text)
            
            return {
                'extracted_text': ocr_result.text,
                'ocr_confidence': ocr_result.confidence,
                'patterns_found': fraud_analysis,
                'text_regions': len(ocr_result.bounding_boxes)
            }
        
        except Exception as e:
            logger.error(f"Screenshot analysis failed: {str(e)}")
            return {}
    
    def _assess_overall_risk(
        self, 
        webpage: WebPage, 
        domain_intel: DomainIntelligence, 
        url_analysis: Dict[str, Any], 
        content_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess overall risk score and classification"""
        risk_score = 0.0
        risk_factors = []
        
        # URL-based risk factors
        url_indicators = url_analysis.get('suspicious_indicators', [])
        risk_score += len(url_indicators) * 0.1
        risk_factors.extend(url_indicators)
        
        # Domain-based risk factors
        if domain_intel:
            domain_score = 1.0 - domain_intel.reputation_score
            risk_score += domain_score * 0.3
            risk_factors.extend(domain_intel.risk_indicators)
        
        # Content-based risk factors
        fraud_indicators = content_analysis.get('fraud_indicators', [])
        risk_score += len(fraud_indicators) * 0.05
        risk_factors.extend(fraud_indicators)
        
        # Form-based risk factors
        form_analysis = content_analysis.get('form_analysis', {})
        sensitive_data = form_analysis.get('sensitive_data_requested', [])
        risk_score += len(sensitive_data) * 0.15
        
        # Normalize risk score
        risk_score = min(1.0, risk_score)
        
        # Classify risk level
        if risk_score >= 0.7:
            risk_level = "HIGH"
        elif risk_score >= 0.4:
            risk_level = "MEDIUM"
        elif risk_score >= 0.2:
            risk_level = "LOW"
        else:
            risk_level = "MINIMAL"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': list(set(risk_factors)),
            'recommendation': self._get_risk_recommendation(risk_level),
            'confidence': 0.8  # Static confidence for now
        }
    
    def _get_risk_recommendation(self, risk_level: str) -> str:
        """Get recommendation based on risk level"""
        recommendations = {
            "HIGH": "DO NOT INTERACT - This appears to be a high-risk website with multiple fraud indicators. Avoid providing any personal information.",
            "MEDIUM": "EXERCISE CAUTION - This website shows several concerning indicators. Verify legitimacy through independent channels before proceeding.",
            "LOW": "PROCEED WITH CAUTION - Some minor risk indicators detected. Verify the website's authenticity if requesting sensitive information.",
            "MINIMAL": "LOW RISK - No significant risk indicators detected, but always exercise normal internet safety practices."
        }
        
        return recommendations.get(risk_level, "Unable to assess risk level.")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.browser:
            await self.browser.close()


# Convenience functions
async def investigate_website(url: str) -> Dict[str, Any]:
    """
    Convenience function for website investigation
    
    Args:
        url: URL to investigate
        
    Returns:
        Comprehensive investigation report
    """
    engine = WebIntelligenceEngine()
    try:
        await engine.initialize()
        return await engine.investigate_url(url)
    finally:
        await engine.cleanup()


async def analyze_domain_safety(domain: str) -> DomainIntelligence:
    """
    Convenience function for domain analysis
    
    Args:
        domain: Domain to analyze
        
    Returns:
        Domain intelligence data
    """
    analyzer = DomainAnalyzer()
    return await analyzer.analyze_domain(domain)
