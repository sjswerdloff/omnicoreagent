import asyncio
import os
from omnicoreagent.community import (
    ExaSearch,
    PerplexitySearch,
    Firecrawl,
    Valyu,
    TakoSearch,
    LocalPython,
    LocalBash
)

async def verify_tools():
    print("Verifying Community Tools...")
    
    # 1. Verify Instantiation (checks for API keys)
    print("\n[1] Checking Tool Instantiation...")
    
    tools_to_check = [
        ("ExaSearch", ExaSearch, "EXA_API_KEY"),
        ("PerplexitySearch", PerplexitySearch, "PERPLEXITY_API_KEY"),
        ("Firecrawl", Firecrawl, "FIRECRAWL_API_KEY"),
        ("Valyu", Valyu, "VALYU_API_KEY"),
        ("TakoSearch", TakoSearch, "TAKO_API_KEY"),
    ]

    for name, cls, env_var in tools_to_check:
        try:
            # We expect this to fail if env var is missing, which confirms validation works
            if not os.environ.get(env_var):
                try:
                    cls()
                    print(f"❌ {name}: Instantiated without API key (Unexpected)")
                except ValueError as e:
                    print(f"✅ {name}: Correctly raised ValueError (missing API key)")
            else:
                cls()
                print(f"✅ {name}: Instantiated successfully with env var")
        except Exception as e:
             print(f"❌ {name}: Failed with unexpected error: {e}")

    # 2. Verify Execution Tools (No API key needed)
    print("\n[2] Checking Execution Tools...")
    
    try:
        python_tool = LocalPython()
        tool = python_tool.get_tool()
        print(f"✅ LocalPython: Tool created ({tool.name})")
        
        # Dry run execution check
        result = python_tool._execute("print('Hello World')")
        
        # Verify dictionary structure
        if isinstance(result, dict) and "status" in result and "data" in result:
             if result["status"] == "success" and "Hello World" in result["data"]:
                print(f"✅ LocalPython: Execution successful (Status: {result['status']})")
             else:
                print(f"❌ LocalPython: Execution failed - {result}")
        else:
             print(f"❌ LocalPython: Invalid response format - {type(result)}")

    except Exception as e:
        print(f"❌ LocalPython: Failed - {e}")

    try:
        bash_tool = LocalBash()
        tool = bash_tool.get_tool()
        print(f"✅ LocalBash: Tool created ({tool.name})")
        
        # Dry run execution check
        result = bash_tool._execute("echo 'Hello Bash'")
        
        # Verify dictionary structure
        if isinstance(result, dict) and "status" in result and "data" in result:
             if result["status"] == "success" and "Hello Bash" in result["data"]:
                 print(f"✅ LocalBash: Execution successful (Status: {result['status']})")
             else:
                 print(f"❌ LocalBash: Execution failed - {result}")
        else:
             print(f"❌ LocalBash: Invalid response format - {type(result)}")

    except Exception as e:
        print(f"❌ LocalBash: Failed - {e}")

if __name__ == "__main__":
    asyncio.run(verify_tools())
