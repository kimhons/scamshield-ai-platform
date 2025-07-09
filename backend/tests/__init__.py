"""
ScamShield AI - Test Suite

Comprehensive test suite for the ScamShield AI backend.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Test configuration
TEST_DATABASE_URL = 'sqlite:///:memory:'
