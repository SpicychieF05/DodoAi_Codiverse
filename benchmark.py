import asyncio
import time
import os
from dotenv import load_dotenv
from multi_api_client import MultiAPIClient

load_dotenv()

async def benchmark():
    print(f"Groq Key present: {bool(os.getenv('GROQ_API_KEY'))}")
    print(f"OpenRouter Key present: {bool(os.getenv('OPENROUTER_API_KEY'))}")
    print(f"Gemini Key present: {bool(os.getenv('GOOGLE_API_KEY'))}")

    client = MultiAPIClient()
    results = []
    
    print("Starting benchmark...")
    
    test_message = "Hi"
    
    for name, provider in client.providers.items():
        print(f"Testing {name}...")
        try:
            start = time.time()
            await provider.chat(test_message)
            duration = time.time() - start
            results.append((name, duration))
            print(f"✅ {name}: {duration:.4f}s")
        except Exception as e:
            print(f"❌ {name} failed: {type(e).__name__}: {e}")
            results.append((name, float('inf')))

    results.sort(key=lambda x: x[1])
    
    print("\n🏆 Fastest APIs:")
    for name, duration in results:
        print(f"{name}: {duration}")

if __name__ == "__main__":
    asyncio.run(benchmark())
