"""
Test script for the FastAPI Document Management Service
Demonstrates usage of all endpoints
"""

import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

# Test data
TEST_FOLDER = "./test_documents"


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_response(response):
    """Pretty print API response"""
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_health_check():
    """Test health check endpoint"""
    print_section("Test 1: Health Check")

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print_response(response)


def test_root_endpoint():
    """Test root endpoint"""
    print_section("Test 2: Root Endpoint")

    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print_response(response)


def test_upload_documents():
    """Test document upload"""
    print_section("Test 3: Upload Documents")

    # Create test documents if they don't exist
    test_folder = Path(TEST_FOLDER)
    test_folder.mkdir(exist_ok=True)

    # Create sample test files
    sample_files = {
        "sample1.txt": "Machine learning is a subset of artificial intelligence.\n"
                      "It focuses on the ability of computers to learn from data.",
        "sample2.txt": "Python is a popular programming language for data science.\n"
                      "It provides excellent libraries like pandas, numpy, and scikit-learn."
    }

    for filename, content in sample_files.items():
        filepath = test_folder / filename
        filepath.write_text(content)

    # Upload files
    files = [
        ("files", open(test_folder / "sample1.txt", "rb")),
        ("files", open(test_folder / "sample2.txt", "rb"))
    ]

    response = requests.post(f"{BASE_URL}/upload", files=files)
    print(f"Status: {response.status_code}")
    print_response(response)

    # Close files
    for _, file_obj in files:
        file_obj.close()


def test_create_index():
    """Test index creation"""
    print_section("Test 4: Create Index")

    payload = {
        "index_name": "test_index",
        "data_folder": "C:/temp/data"
    }

    response = requests.post(
        f"{BASE_URL}/index",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print_response(response)


def test_search_documents():
    """Test document search"""
    print_section("Test 5: Search Documents")

    payload = {
        "query": "machine learning",
        "index_name": "test_index",
        "top_k": 5
    }

    response = requests.post(
        f"{BASE_URL}/search",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print_response(response)


def test_ask_question():
    """Test Q&A functionality"""
    print_section("Test 6: Ask Question")

    payload = {
        "question": "What is machine learning?",
        "index_name": "test_index"
    }

    response = requests.post(
        f"{BASE_URL}/ask",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print_response(response)


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  FastAPI Document Management Service - Test Suite")
    print("=" * 60)

    try:
        test_health_check()
        test_root_endpoint()
        test_upload_documents()
        test_create_index()
        test_search_documents()
        test_ask_question()

        print_section("All Tests Completed")
        print("✓ Test suite completed successfully")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the API server")
        print("   Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    run_all_tests()

