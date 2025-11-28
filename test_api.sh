#!/bin/bash

# API Testing Script
BASE_URL="http://localhost:8000"

echo "==================================="
echo "Online Poll System - API Test"
echo "==================================="
echo ""

# Test 1: List Polls
echo "1. Testing GET /api/polls/ (List active polls)"
curl -s -X GET "$BASE_URL/api/polls/" | python -m json.tool
echo ""
echo ""

# Test 2: Create Poll (requires authentication)
echo "2. Testing POST /api/polls/ (Create poll)"
echo "Note: This requires JWT token. Get token first with:"
echo "curl -X POST $BASE_URL/api/token/ -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"your-password\"}'"
echo ""

# Test 3: Vote on Poll
echo "3. Testing POST /api/polls/1/vote/ (Vote on poll)"
curl -s -X POST "$BASE_URL/api/polls/1/vote/" \
  -H "Content-Type: application/json" \
  -d '{
    "choice_id": 1,
    "voter_identifier": "test@example.com"
  }' | python -m json.tool
echo ""
echo ""

# Test 4: Get Results
echo "4. Testing GET /api/polls/1/results/ (Get poll results)"
curl -s -X GET "$BASE_URL/api/polls/1/results/" | python -m json.tool
echo ""
echo ""

# Test 5: Swagger Documentation
echo "5. API Documentation available at:"
echo "   - Swagger UI: $BASE_URL/swagger/"
echo "   - ReDoc: $BASE_URL/redoc/"
echo "   - Admin Panel: $BASE_URL/admin/"
echo ""

echo "==================================="
echo "Test Complete!"
echo "==================================="
