"""
Test script to validate all fixes in multi_api_client.py
"""
from multi_api_client import MultiAPIClient

def test_initialization():
    print("="*80)
    print("Testing MultiAPIClient Initialization")
    print("="*80)
    
    try:
        client = MultiAPIClient()
        print("✅ Initialization successful")
        
        print(f"\n📊 Providers: {len(client.providers)}")
        for k, v in client.providers.items():
            print(f"  - {k}: {v.model}")
        
        print(f"\n🎯 Tier Priorities:")
        for tier, providers in client.tier_priorities.items():
            if len(providers) > 3:
                print(f"  {tier}: {providers[:3]}...")
            else:
                print(f"  {tier}: {providers}")
        
        print(f"\n⚡ RPM Limits:")
        for provider, limit in client.rpm_limits.items():
            print(f"  {provider}: {limit} RPM")
        
        print("\n" + "="*80)
        print("Testing Query Classification")
        print("="*80)
        
        test_queries = [
            ("What is AI?", "simple"),
            ("Explain machine learning concepts", "medium"),
            ("Provide comprehensive analysis with step-by-step reasoning", "complex")
        ]
        
        for query, expected in test_queries:
            result = client.classify_query(query)
            status = "✅" if result == expected else "❌"
            print(f"{status} '{query[:50]}...' → {result} (expected: {expected})")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_initialization()
    exit(0 if success else 1)
