import asyncio
from omnicoreagent import DeepAgent


async def main():
    """Basic DeepAgent example - works for any domain."""

    # Your system_instruction defines the domain
    agent = DeepAgent(
        name="DataAnalyst",
        system_instruction="""
You are a senior data analyst.
You excel at breaking down complex analysis tasks and producing insights.
""",
        model_config={
            "provider": "openai",
            "model": "gpt-4o",
        },
    )

    await agent.initialize()
    print(f"✓ Initialized: {agent.name}")

    # For complex tasks, agent can spawn subagents automatically
    print("\n🚀 Running agent...")
    result = await agent.run("""
    Analyze the key factors affecting sales performance.
    Consider: seasonal trends, regional differences, product categories.
    """)

    print(f"\n📋 Result:\n{result['response'][:800]}...")

    await agent.cleanup()
    print("\n✓ Done")


if __name__ == "__main__":
    asyncio.run(main())
