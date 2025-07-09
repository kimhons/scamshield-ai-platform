"""
ScamShield AI - Advanced OCR Engine

Comprehensive OCR capabilities with multiple backends, language support, and 
intelligent text extraction for fraud investigation.
"""

import cv2
import numpy as np
import pytesseract
import easyocr
import base64
import io
import re
import json
from PIL import Image, ImageEnhance, ImageFilter
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import asyncio
import concurrent.futures
from pathlib import Path

from ..utils.error_handler import ErrorContext, APIError
from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class OCREngine(Enum):
    """Available OCR engines"""
    TESSERACT = "tesseract"
    EASYOCR = "easyocr"
    HYBRID = "hybrid"


class ImageQuality(Enum):
    """Image quality assessment"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


@dataclass
class OCRResult:
    """OCR extraction result"""
    text: str
    confidence: float
    bounding_boxes: List[Dict[str, Any]]
    language: str
    processing_time: float
    engine_used: str
    image_quality: ImageQuality
    metadata: Dict[str, Any]


@dataclass
class TextRegion:
    """Detected text region"""
    text: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x, y, width, height
    language: str


class ImagePreprocessor:
    """Advanced image preprocessing for OCR optimization"""
    
    def __init__(self):
        self.filters = {
            'noise_reduction': self._apply_noise_reduction,
            'contrast_enhancement': self._enhance_contrast,
            'sharpening': self._apply_sharpening,
            'deskewing': self._deskew_image,
            'binarization': self._apply_binarization,
            'morphological': self._apply_morphological_operations
        }
    
    def preprocess_image(
        self, 
        image: np.ndarray, 
        filters: List[str] = None,
        auto_enhance: bool = True
    ) -> np.ndarray:
        """
        Apply preprocessing filters to optimize image for OCR
        
        Args:
            image: Input image as numpy array
            filters: List of filters to apply
            auto_enhance: Automatically select optimal filters
            
        Returns:
            Preprocessed image
        """
        with ErrorContext("image_preprocessing"):
            processed_image = image.copy()
            
            if auto_enhance:
                filters = self._select_optimal_filters(image)
            elif filters is None:
                filters = ['noise_reduction', 'contrast_enhancement', 'binarization']
            
            for filter_name in filters:
                if filter_name in self.filters:
                    try:
                        processed_image = self.filters[filter_name](processed_image)
                        logger.debug(f"Applied filter: {filter_name}")
                    except Exception as e:
                        logger.warning(f"Filter {filter_name} failed: {str(e)}")
                        continue
            
            return processed_image
    
    def _select_optimal_filters(self, image: np.ndarray) -> List[str]:
        """Automatically select optimal preprocessing filters"""
        filters = []
        
        # Analyze image characteristics
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Check if image needs noise reduction
        noise_level = self._estimate_noise_level(gray)
        if noise_level > 0.1:
            filters.append('noise_reduction')
        
        # Check contrast
        contrast = np.std(gray)
        if contrast < 50:
            filters.append('contrast_enhancement')
        
        # Check if image is skewed
        if self._detect_skew(gray) > 2:
            filters.append('deskewing')
        
        # Always apply binarization for text
        filters.append('binarization')
        
        # Apply sharpening if image is blurry
        if self._detect_blur(gray) > 100:
            filters.append('sharpening')
        
        return filters
    
    def _apply_noise_reduction(self, image: np.ndarray) -> np.ndarray:
        """Apply noise reduction using bilateral filter"""
        if len(image.shape) == 3:
            return cv2.bilateralFilter(image, 9, 75, 75)
        else:
            return cv2.bilateralFilter(image, 9, 75, 75)
    
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Enhance image contrast using CLAHE"""
        if len(image.shape) == 3:
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            enhanced = cv2.merge([l, a, b])
            return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        else:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            return clahe.apply(image)
    
    def _apply_sharpening(self, image: np.ndarray) -> np.ndarray:
        """Apply sharpening filter"""
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)
    
    def _deskew_image(self, image: np.ndarray) -> np.ndarray:
        """Correct image skew using Hough transform"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Detect edges
        edges = cv2.Canny(gray, 100, 100, apertureSize=3)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is not None:
            # Calculate average angle
            angles = []
            for rho, theta in lines[:, 0]:
                angle = np.degrees(theta) - 90
                angles.append(angle)
            
            if angles:
                angle = np.median(angles)
                
                # Rotate image to correct skew
                if abs(angle) > 0.5:  # Only correct if significant skew
                    rows, cols = gray.shape
                    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
                    
                    if len(image.shape) == 3:
                        return cv2.warpAffine(image, M, (cols, rows))
                    else:
                        return cv2.warpAffine(image, M, (cols, rows))
        
        return image
    
    def _apply_binarization(self, image: np.ndarray) -> np.ndarray:
        """Apply adaptive thresholding for binarization"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Try different binarization methods and select best
        methods = [
            ('otsu', lambda: cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
            ('adaptive_mean', lambda: cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)),
            ('adaptive_gaussian', lambda: cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2))
        ]
        
        best_result = None
        best_score = 0
        
        for method_name, method_func in methods:
            try:
                result = method_func()
                score = self._evaluate_binarization_quality(result)
                if score > best_score:
                    best_score = score
                    best_result = result
            except Exception:
                continue
        
        return best_result if best_result is not None else gray
    
    def _apply_morphological_operations(self, image: np.ndarray) -> np.ndarray:
        """Apply morphological operations to clean up text"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Define kernel for morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        
        # Apply opening to remove noise
        opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        
        # Apply closing to fill gaps
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        
        return closing
    
    def _estimate_noise_level(self, image: np.ndarray) -> float:
        """Estimate noise level in image"""
        laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
        return 1.0 / (1.0 + laplacian_var / 1000.0)
    
    def _detect_skew(self, image: np.ndarray) -> float:
        """Detect image skew angle"""
        edges = cv2.Canny(image, 100, 100, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is not None:
            angles = []
            for rho, theta in lines[:, 0]:
                angle = np.degrees(theta) - 90
                angles.append(angle)
            
            if angles:
                return abs(np.median(angles))
        
        return 0.0
    
    def _detect_blur(self, image: np.ndarray) -> float:
        """Detect image blur using Laplacian variance"""
        return cv2.Laplacian(image, cv2.CV_64F).var()
    
    def _evaluate_binarization_quality(self, binary_image: np.ndarray) -> float:
        """Evaluate quality of binarization"""
        # Calculate ratio of black to white pixels (should be balanced for text)
        white_pixels = np.sum(binary_image == 255)
        black_pixels = np.sum(binary_image == 0)
        total_pixels = binary_image.size
        
        # Ideal ratio for text is around 10-20% black pixels
        black_ratio = black_pixels / total_pixels
        if 0.05 <= black_ratio <= 0.3:
            return 1.0 - abs(0.15 - black_ratio) * 5
        else:
            return 0.1
    
    def assess_image_quality(self, image: np.ndarray) -> ImageQuality:
        """Assess overall image quality for OCR"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Calculate various quality metrics
        blur_score = self._detect_blur(gray)
        noise_score = 1.0 - self._estimate_noise_level(gray)
        contrast_score = np.std(gray) / 255.0
        
        # Combine scores
        overall_score = (blur_score/1000 + noise_score + contrast_score) / 3
        
        if overall_score > 0.7:
            return ImageQuality.EXCELLENT
        elif overall_score > 0.5:
            return ImageQuality.GOOD
        elif overall_score > 0.3:
            return ImageQuality.FAIR
        else:
            return ImageQuality.POOR


class AdvancedOCREngine:
    """Advanced OCR engine with multiple backends and intelligent processing"""
    
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.easyocr_reader = None
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'ru': 'Russian'
        }
        
        # Initialize EasyOCR reader lazily
        self._init_easyocr()
    
    def _init_easyocr(self):
        """Initialize EasyOCR reader"""
        try:
            import easyocr
            self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
            logger.info("EasyOCR initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize EasyOCR: {str(e)}")
            self.easyocr_reader = None
    
    async def extract_text(
        self,
        image_input: Union[str, bytes, np.ndarray],
        engine: OCREngine = OCREngine.HYBRID,
        languages: List[str] = None,
        preprocess: bool = True,
        confidence_threshold: float = 0.5
    ) -> OCRResult:
        """
        Extract text from image using specified OCR engine
        
        Args:
            image_input: Image data (path, bytes, or numpy array)
            engine: OCR engine to use
            languages: Languages to detect (default: ['en'])
            preprocess: Apply image preprocessing
            confidence_threshold: Minimum confidence for text extraction
            
        Returns:
            OCR extraction result
        """
        with ErrorContext("ocr_text_extraction"):
            start_time = asyncio.get_event_loop().time()
            
            # Load and prepare image
            image = self._load_image(image_input)
            
            # Assess image quality
            image_quality = self.preprocessor.assess_image_quality(image)
            
            # Preprocess image if needed
            if preprocess:
                image = self.preprocessor.preprocess_image(image, auto_enhance=True)
            
            # Set default languages
            if languages is None:
                languages = ['en']
            
            # Extract text using specified engine
            if engine == OCREngine.TESSERACT:
                result = await self._extract_with_tesseract(image, languages, confidence_threshold)
            elif engine == OCREngine.EASYOCR:
                result = await self._extract_with_easyocr(image, languages, confidence_threshold)
            elif engine == OCREngine.HYBRID:
                result = await self._extract_with_hybrid(image, languages, confidence_threshold)
            else:
                raise APIError(f"Unsupported OCR engine: {engine}")
            
            # Calculate processing time
            processing_time = asyncio.get_event_loop().time() - start_time
            
            # Create comprehensive result
            ocr_result = OCRResult(
                text=result['text'],
                confidence=result['confidence'],
                bounding_boxes=result['bounding_boxes'],
                language=result['language'],
                processing_time=processing_time,
                engine_used=engine.value,
                image_quality=image_quality,
                metadata={
                    'image_shape': image.shape,
                    'preprocessing_applied': preprocess,
                    'languages_detected': result.get('languages_detected', languages),
                    'text_regions_count': len(result['bounding_boxes'])
                }
            )
            
            logger.info("OCR extraction completed",
                       engine=engine.value,
                       processing_time=processing_time,
                       confidence=result['confidence'],
                       text_length=len(result['text']))
            
            return ocr_result
    
    async def _extract_with_tesseract(
        self, 
        image: np.ndarray, 
        languages: List[str],
        confidence_threshold: float
    ) -> Dict[str, Any]:
        """Extract text using Tesseract OCR"""
        # Configure Tesseract
        config = '--oem 3 --psm 6'
        lang_param = '+'.join(languages)
        
        # Extract text with confidence scores
        data = pytesseract.image_to_data(
            image, 
            lang=lang_param, 
            config=config, 
            output_type=pytesseract.Output.DICT
        )
        
        # Filter high-confidence text
        text_parts = []
        bounding_boxes = []
        confidences = []
        
        for i, confidence in enumerate(data['conf']):
            if confidence != -1 and confidence >= confidence_threshold * 100:
                text = data['text'][i].strip()
                if text:
                    text_parts.append(text)
                    confidences.append(confidence / 100.0)
                    
                    # Add bounding box
                    bbox = {
                        'text': text,
                        'confidence': confidence / 100.0,
                        'bbox': [
                            data['left'][i],
                            data['top'][i],
                            data['width'][i],
                            data['height'][i]
                        ]
                    }
                    bounding_boxes.append(bbox)
        
        # Combine text and calculate average confidence
        full_text = ' '.join(text_parts)
        avg_confidence = np.mean(confidences) if confidences else 0.0
        
        return {
            'text': full_text,
            'confidence': avg_confidence,
            'bounding_boxes': bounding_boxes,
            'language': languages[0] if languages else 'en'
        }
    
    async def _extract_with_easyocr(
        self, 
        image: np.ndarray, 
        languages: List[str],
        confidence_threshold: float
    ) -> Dict[str, Any]:
        """Extract text using EasyOCR"""
        if self.easyocr_reader is None:
            raise APIError("EasyOCR is not available")
        
        # Reinitialize reader with specified languages if needed
        if languages != ['en']:
            try:
                import easyocr
                self.easyocr_reader = easyocr.Reader(languages, gpu=False)
            except Exception as e:
                logger.warning(f"Failed to reinitialize EasyOCR with languages {languages}: {str(e)}")
        
        # Extract text
        results = self.easyocr_reader.readtext(image)
        
        # Process results
        text_parts = []
        bounding_boxes = []
        confidences = []
        
        for (bbox_coords, text, confidence) in results:
            if confidence >= confidence_threshold:
                text_parts.append(text)
                confidences.append(confidence)
                
                # Convert bbox coordinates
                x_coords = [point[0] for point in bbox_coords]
                y_coords = [point[1] for point in bbox_coords]
                
                bbox = {
                    'text': text,
                    'confidence': confidence,
                    'bbox': [
                        min(x_coords),
                        min(y_coords),
                        max(x_coords) - min(x_coords),
                        max(y_coords) - min(y_coords)
                    ]
                }
                bounding_boxes.append(bbox)
        
        # Combine results
        full_text = ' '.join(text_parts)
        avg_confidence = np.mean(confidences) if confidences else 0.0
        
        return {
            'text': full_text,
            'confidence': avg_confidence,
            'bounding_boxes': bounding_boxes,
            'language': languages[0] if languages else 'en'
        }
    
    async def _extract_with_hybrid(
        self, 
        image: np.ndarray, 
        languages: List[str],
        confidence_threshold: float
    ) -> Dict[str, Any]:
        """Extract text using hybrid approach (multiple engines)"""
        # Run both engines in parallel
        tasks = []
        
        # Tesseract
        tasks.append(self._extract_with_tesseract(image, languages, confidence_threshold))
        
        # EasyOCR (if available)
        if self.easyocr_reader is not None:
            tasks.append(self._extract_with_easyocr(image, languages, confidence_threshold))
        
        # Execute tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        valid_results = [r for r in results if not isinstance(r, Exception)]
        
        if not valid_results:
            raise APIError("All OCR engines failed")
        
        # Select best result based on confidence and text length
        best_result = max(valid_results, key=lambda r: r['confidence'] * len(r['text']))
        
        # Merge bounding boxes from all engines for comprehensive detection
        all_bboxes = []
        for result in valid_results:
            all_bboxes.extend(result['bounding_boxes'])
        
        # Remove duplicates and merge nearby boxes
        merged_bboxes = self._merge_bounding_boxes(all_bboxes)
        
        return {
            'text': best_result['text'],
            'confidence': best_result['confidence'],
            'bounding_boxes': merged_bboxes,
            'language': best_result['language'],
            'languages_detected': languages
        }
    
    def _merge_bounding_boxes(self, bboxes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge overlapping bounding boxes"""
        if not bboxes:
            return []
        
        # Sort by x coordinate
        sorted_bboxes = sorted(bboxes, key=lambda b: b['bbox'][0])
        
        merged = []
        current = sorted_bboxes[0]
        
        for bbox in sorted_bboxes[1:]:
            # Check if boxes overlap or are close
            if self._boxes_overlap_or_close(current['bbox'], bbox['bbox']):
                # Merge boxes
                current = self._merge_two_boxes(current, bbox)
            else:
                merged.append(current)
                current = bbox
        
        merged.append(current)
        return merged
    
    def _boxes_overlap_or_close(self, box1: List[int], box2: List[int], threshold: int = 10) -> bool:
        """Check if two bounding boxes overlap or are close"""
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        
        # Calculate overlap
        overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
        overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
        
        # Check if close enough
        distance = ((x1 + w1/2 - x2 - w2/2)**2 + (y1 + h1/2 - y2 - h2/2)**2)**0.5
        
        return overlap_x > 0 and overlap_y > 0 or distance < threshold
    
    def _merge_two_boxes(self, box1: Dict[str, Any], box2: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two bounding boxes"""
        x1, y1, w1, h1 = box1['bbox']
        x2, y2, w2, h2 = box2['bbox']
        
        # Calculate merged box coordinates
        min_x = min(x1, x2)
        min_y = min(y1, y2)
        max_x = max(x1 + w1, x2 + w2)
        max_y = max(y1 + h1, y2 + h2)
        
        # Merge text and confidence
        merged_text = f"{box1['text']} {box2['text']}"
        merged_confidence = (box1['confidence'] + box2['confidence']) / 2
        
        return {
            'text': merged_text,
            'confidence': merged_confidence,
            'bbox': [min_x, min_y, max_x - min_x, max_y - min_y]
        }
    
    def _load_image(self, image_input: Union[str, bytes, np.ndarray]) -> np.ndarray:
        """Load image from various input formats"""
        if isinstance(image_input, str):
            # File path
            if Path(image_input).exists():
                return cv2.imread(image_input)
            else:
                # Base64 string
                try:
                    image_data = base64.b64decode(image_input)
                    nparr = np.frombuffer(image_data, np.uint8)
                    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                except Exception:
                    raise APIError("Invalid image data or file path")
        
        elif isinstance(image_input, bytes):
            # Raw bytes
            nparr = np.frombuffer(image_input, np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        elif isinstance(image_input, np.ndarray):
            # Already a numpy array
            return image_input
        
        else:
            raise APIError("Unsupported image input format")
    
    def extract_specific_patterns(self, text: str) -> Dict[str, List[str]]:
        """Extract specific patterns from OCR text (emails, phones, URLs, etc.)"""
        patterns = {
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phones': r'[\+]?[1-9]?[0-9]{7,15}',
            'urls': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            'credit_cards': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'social_security': r'\b\d{3}-\d{2}-\d{4}\b',
            'addresses': r'\d+\s+[A-Za-z0-9\s,]+\b(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)\b',
            'dates': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
            'amounts': r'\$\d+(?:,\d{3})*(?:\.\d{2})?',
            'bitcoin_addresses': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
            'ip_addresses': r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        }
        
        extracted = {}
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            extracted[pattern_name] = list(set(matches))  # Remove duplicates
        
        return extracted


# Convenience functions
async def extract_text_from_image(
    image_input: Union[str, bytes, np.ndarray],
    engine: str = "hybrid",
    languages: List[str] = None,
    confidence_threshold: float = 0.5
) -> OCRResult:
    """
    Convenience function for text extraction
    
    Args:
        image_input: Image data
        engine: OCR engine ("tesseract", "easyocr", "hybrid")
        languages: Languages to detect
        confidence_threshold: Minimum confidence
        
    Returns:
        OCR extraction result
    """
    ocr_engine = AdvancedOCREngine()
    engine_enum = OCREngine(engine)
    
    return await ocr_engine.extract_text(
        image_input=image_input,
        engine=engine_enum,
        languages=languages or ['en'],
        confidence_threshold=confidence_threshold
    )


def extract_fraud_indicators(text: str) -> Dict[str, Any]:
    """
    Extract potential fraud indicators from OCR text
    
    Args:
        text: Extracted text from OCR
        
    Returns:
        Dictionary of potential fraud indicators
    """
    ocr_engine = AdvancedOCREngine()
    patterns = ocr_engine.extract_specific_patterns(text)
    
    # Fraud-specific analysis
    fraud_keywords = [
        'urgent', 'act now', 'limited time', 'guarantee', 'risk-free',
        'winner', 'congratulations', 'cash prize', 'inheritance',
        'verify account', 'suspended', 'click here', 'download now',
        'free money', 'easy money', 'work from home', 'investment opportunity'
    ]
    
    found_keywords = [keyword for keyword in fraud_keywords if keyword.lower() in text.lower()]
    
    return {
        'extracted_patterns': patterns,
        'fraud_keywords': found_keywords,
        'risk_score': len(found_keywords) / len(fraud_keywords),
        'suspicious_patterns': {
            'multiple_emails': len(patterns.get('emails', [])) > 3,
            'multiple_phones': len(patterns.get('phones', [])) > 2,
            'bitcoin_addresses': len(patterns.get('bitcoin_addresses', [])) > 0,
            'suspicious_urls': any('bit.ly' in url or 'tinyurl' in url for url in patterns.get('urls', [])),
            'urgent_language': any(keyword in text.lower() for keyword in ['urgent', 'immediate', 'act now'])
        }
    }
