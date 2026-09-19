"""
user_attribute_inference_langchain_gemini.py
-------------------------------------------
Uses LangChain + Google Gemini 2.5 Flash (cloud-hosted) to infer:
  - age_bracket
  - geography
  - language
  - professional_interests

Install:
    pip install langchain-google-genai pydantic

Set your API key:
    export GOOGLE_API_KEY="..."
    # or on Windows: set GOOGLE_API_KEY=...
"""

from __future__ import annotations

import os
from enum import Enum
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# ----------------------------------------------------------------------
# Structured output schema
# ----------------------------------------------------------------------
class AgeBracket(str, Enum):
    UNDER_18 = "under_18"
    AGE_18_24 = "18-24"
    AGE_25_34 = "25-34"
    AGE_35_44 = "35-44"
    AGE_45_54 = "45-54"
    AGE_55_PLUS = "55+"
    UNKNOWN = "unknown"


class UserAttributes(BaseModel):
    """Inferred user attributes from a handle and comment."""
    age_bracket: AgeBracket = Field(
        description="Inferred age bracket based on handle and comment."
    )
    geography: str = Field(
        description="Inferred country or region (e.g., 'United States', 'India'). "
                    "Use 'unknown' if uncertain."
    )
    language: str = Field(
        description="Primary language of the comment (e.g., 'English', 'Hindi')."
    )
    professional_interests: List[str] = Field(
        description="1-3 likely professional fields or interests "
                    "(e.g., ['technology', 'software_engineering']). "
                    "Empty list if unknown."
    )


# ----------------------------------------------------------------------
# LangChain model + chain
# ----------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert at inferring user attributes from social media data.
Given a user handle and a comment, infer the requested attributes.

Rules:
- Base your inference ONLY on the provided handle and comment.
- If uncertain, use "unknown" or an empty list.
- Do NOT make up information not supported by the text.
"""

USER_TEMPLATE = """User Handle: {handle}
Comment: {comment}"""


def build_chain(model_name: str = "gemini-2.5-flash"):
    """
    Build a LangChain chain that returns structured UserAttributes.

    Uses Google's Gemini 2.5 Flash model via LangChain's
    ChatGoogleGenerativeAI integration.

    The 'json_schema' method uses Gemini's native structured output API,
    which constrains generation directly (more reliable than function
    calling for this task).
    """
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.1,
        max_tokens=512,
    )

    # with_structured_output binds the Pydantic schema to the model.
    # method="json_schema" uses Gemini's native controlled generation.
    structured_llm = llm.with_structured_output(
        UserAttributes,
        method="json_schema"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", USER_TEMPLATE),
    ])

    # LCEL pipe: prompt -> structured LLM -> validated Pydantic object
    return prompt | structured_llm


# ----------------------------------------------------------------------
# Interactive CLI
# ----------------------------------------------------------------------
def main():
    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY environment variable is not set.")
        print("Get a free key at https://aistudio.google.com/app/apikey")
        print("  export GOOGLE_API_KEY='...'   (Linux/macOS)")
        print("  set GOOGLE_API_KEY=...        (Windows CMD)")
        return

    print("Building chain (Gemini 2.5 Flash)...")
    chain = build_chain()

    print("=" * 70)
    print("User Attribute Inference (LangChain + Google Gemini)")
    print("Model: gemini-2.5-flash")
    print("=" * 70)
    print("Enter a user handle and a comment. Type 'quit' to exit.\n")

    while True:
        try:
            handle = input("User Handle > ").strip()
            if handle.lower() in {"quit", "exit"}:
                print("Bye!")
                break
            if not handle:
                print("(empty handle — try again)")
                continue

            comment = input("Comment     > ").strip()
            if comment.lower() in {"quit", "exit"}:
                print("Bye!")
                break
            if not comment:
                print("(empty comment — try again)")
                continue
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        print("\nInferring via LangChain + Gemini...")
        try:
            attrs: UserAttributes = chain.invoke({
                "handle": handle,
                "comment": comment,
            })
        except Exception as e:
            print(f"[Error] {type(e).__name__}: {e}")
            continue

        print("\n" + "-" * 70)
        print("INFERRED ATTRIBUTES")
        print("-" * 70)
        print(f"  Age Bracket            : {attrs.age_bracket.value}")
        print(f"  Geography              : {attrs.geography}")
        print(f"  Language               : {attrs.language}")
        print(f"  Professional Interests : {', '.join(attrs.professional_interests) or '(none)'}")
        print("-" * 70 + "\n")


if __name__ == "__main__":
    main()