"""
Test script to demonstrate the tier-based routing system
"""
import asyncio
from multi_api_client import MultiAPIClient

async def test_tier_routing():
    client = MultiAPIClient()
    
    # Test queries for each complexity tier
    test_queries = {
        'simple': [
            "What is Python?",
            "Hello",
            "What time is it?",
            "Define AI"
        ],
        'medium': [
            "Explain how Python handles memory management",
            "Compare list vs tuple in Python",
            "How does machine learning work?",
            "List the steps to create a REST API"
        ],
        'complex': [
            "Provide a detailed plan with step-by-step reasoning for building a scalable microservices architecture",
            "Analyze deeply the pros and cons of different database systems for a high-traffic web application",
            "Give me a comprehensive analysis of cloud computing architectures with detailed breakdown of each component"
        ]
    }
    
    print("=" * 80)
    print("TIER-BASED ROUTING TEST")
    print("=" * 80)
    
    for expected_tier, queries in test_queries.items():
        print(f"\n{'='*80}")
        print(f"Testing {expected_tier.upper()} Queries")
        print(f"Expected Priority: {client.tier_priorities[expected_tier]}")
        print(f"{'='*80}\n")
        
        for query in queries:
            classified_tier = client.classify_query(query)
            print(f"Query: \"{query[:60]}...\"" if len(query) > 60 else f"Query: \"{query}\"")
            print(f"  Classified as: {classified_tier}")
            print(f"  Priority order: {client.tier_priorities[classified_tier][:3]} ...")
            print(f"  ✓ Correct!" if classified_tier == expected_tier else f"  ✗ Expected: {expected_tier}")
            print()

if __name__ == "__main__":
    asyncio.run(test_tier_routing())
