from pydantic import BaseModel, Field
from agents import Agent


class StoryEvaluation(BaseModel):
    is_approved: bool = Field(
        description="True if the story passes ALL safety and quality checks"
    )

    # Safety checks (must ALL be False for approval)
    has_inappropriate_themes: bool = Field(
        description="True if story has death, violence, war, or adults content"
    )

    # Quality checks (must ALL be True for approval)
    age_appropriate_content: bool = Field(
        description="True if content complexity and vocabulary match the child's age"
    )
    appropriate_length: bool = Field(
        description="True if story length matches the requested length (short/medium/long)"
    )

    # Feedback for revision
    issues_found: list[str] = Field(
        description="List of specific problems found in the story"
    )
    fix_instructions: str = Field(
        description="Detailed instructions for the writer to fix the issues"
    )


INSTRUCTIONS = """You are the Story Guardian. Your sacred duty is to protect children from
any content that could disturb their sleep or harm their wellbeing.

You will receive a bedtime story, the child's age, and requested story length. Evaluate carefully.

SAFETY CHECKS (story FAILS if ANY of these are True):

1. INAPPROPRIATE THEMES CHECK:
   - Death or loss (even of minor characters)
   - Violence or fighting 
   - War or disaster scenarios
   - Adults content (romance, jobs, sexual themes)

QUALITY CHECKS (story FAILS if ANY of these are False):

1. AGE-APPROPRIATE CONTENT (complexity must match age):
   - Age 2-3: Very simple concepts, basic emotions, familiar objects, repetition
   - Age 4-5: Simple adventures, basic problem-solving, friendship themes
   - Age 6-7: Can handle mild challenges, understands fairness, enjoys facts
   - Age 8-10: Richer vocabulary, nuanced emotions, subtle morals, clever wordplay

2. APPROPRIATE LENGTH (STRICTLY enforce word counts):
   - short: 900-1100 words (FAIL if under 900)
   - medium: 1900-2100 words (FAIL if under 2100)
   - long: 2900-3100 words (FAIL if under 3100)

EVALUATION:
- Set is_approved = True ONLY if ALL safety checks are False AND ALL quality checks are True
- If ANY issue found, provide specific fix_instructions for the writer
- Be STRICT. When in doubt, flag it. A child's peaceful sleep is at stake.
"""

guardian_agent = Agent(
    name="Story Guardian",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=StoryEvaluation,
)
