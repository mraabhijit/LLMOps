from config import PROMPT_REGISTRY_NAME
from prompts import PromptRegistry


def main():
    registry = PromptRegistry()
    registry.register(
        name=PROMPT_REGISTRY_NAME,
        version="v1",
        filepath="rag_prompt_v1.txt",
        description="V1 prompt",
        author="system",
    )
    registry.register(
        name=PROMPT_REGISTRY_NAME,
        version="v2",
        filepath="rag_prompt_v2.txt",
        description="V2 prompt",
        author="system",
    )
    registry.set_active(
        name=PROMPT_REGISTRY_NAME,
        version="v1",
    )
    print("Manifest saved to: ", registry.manifest)


if __name__ == "__main__":
    main()
