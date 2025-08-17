#!/usr/bin/env python3
"""
Simple Test Runner for Thales CSM MCP Server
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests with pytest."""
    print("🧪 Running Thales CSM MCP Server Tests")
    print("=" * 50)
    
    # Check if pytest is available
    try:
        import pytest
        print("✅ pytest found")
    except ImportError:
        print("❌ pytest not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest"])
    
    # Run tests
    print("\n🚀 Running tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", "-v", "--tb=short"
    ])
    
    if result.returncode == 0:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check output above.")
    
    return result.returncode

def run_specific_test(test_file):
    """Run a specific test file."""
    print(f"🧪 Running {test_file}")
    print("=" * 50)
    
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        f"tests/{test_file}", "-v", "--tb=short"
    ])
    
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_file = sys.argv[1]
        exit(run_specific_test(test_file))
    else:
        # Run all tests
        exit(run_tests()) 