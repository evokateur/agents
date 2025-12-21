from pydantic import BaseModel, Field
from agents import Runner, trace, gen_trace_id
from planner_agent import planner_agent, StorySearchPlan, StorySearchItem
from research_agent import research_agent
from writer_agent import writer_agent, BedtimeStory
from guardian_agent import guardian_agent, StoryEvaluation
import asyncio


class UserInput(BaseModel):
    child_name: str = Field(description="The child's name - they will be the hero")
    age: int = Field(description="Child's age in years (2-10)")
    story_length: str = Field(
        description="Story length: short (2-3 min), medium (5 min), or long (10 min)"
    )
    interests: list[str] = Field(description="What the child loves")
    special_character: str | None = Field(
        description="Pet, friend, or toy to include in the story"
    )
    moral_lesson: str = Field(description="Life lesson to weave in")
    topics_to_avoid: str | None = Field(description="Anything to avoid in the story")
    include_fun_fact: bool = Field(description="Whether to include an educational fact")


class StoryResult(BaseModel):
    story: BedtimeStory
    evaluation: StoryEvaluation
    revision_attempts: int


class StoryManager:
    MAX_REVISION_ATTEMPTS = 3

    async def run(self, user_input: UserInput):
        """Run the story generation process, yielding status updates and the final story"""
        trace_id = gen_trace_id()
        with trace("DreamWeaver Story Generation", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            )
            yield f"🔗 [View trace](https://platform.openai.com/traces/trace?trace_id={trace_id})"

            # Step 1: Plan searches
            yield "🎨 Planning your magical story..."
            search_plan = await self.plan_searches(user_input)
            yield f"📋 Theme: {search_plan.story_theme}"

            # Step 2: Research inspiration
            yield "🔍 Researching inspiration..."
            research_results = await self.perform_searches(search_plan)
            yield f"✨ Found {len(research_results)} sources of inspiration"

            # Step 3: Write the story
            yield "✍️ Writing your bedtime story..."
            story = await self.write_story(user_input, research_results)
            yield f'📖 Draft complete: "{story.title}"'

            # Step 4: Evaluate and revise loop
            yield "🛡️ Guardian is checking the story..."
            evaluation = await self.evaluate_story(story, user_input)

            attempts = 0
            while not evaluation.is_approved and attempts < self.MAX_REVISION_ATTEMPTS:
                attempts += 1
                yield f"📝 Revising story (attempt {attempts}/{self.MAX_REVISION_ATTEMPTS})..."
                yield f"   Issues: {', '.join(evaluation.issues_found)}"
                story = await self.revise_story(
                    story, evaluation, user_input, research_results
                )
                evaluation = await self.evaluate_story(story, user_input)

            # Final result
            if evaluation.is_approved:
                yield "✅ Story approved by Guardian!"
                yield f"⏱️ Reading time: ~{story.reading_time_minutes} minutes"
                yield f"💝 Moral: {story.moral_lesson}"
                if story.fun_fact_included:
                    yield f"🧠 Fun fact: {story.fun_fact_included}"
                yield "---"
                yield f"# {story.title}\n\n{story.story}"
            else:
                yield "❌ Could not create a safe story after multiple attempts."
                yield "Please try different inputs or avoid certain topics."

    async def plan_searches(self, user_input: UserInput) -> StorySearchPlan:
        """Create search queries based on user input"""
        print("Planning searches...")
        input_text = f"""
=== USER'S ANSWERS ===
שם הילד/ה (Child's Name): {user_input.child_name}
גיל (Age): {user_input.age}
אורך הסיפור (Story Length): {user_input.story_length}
תחומי עניין (Interests): {', '.join(user_input.interests)}
דמות מיוחדת (Special Character): {user_input.special_character or 'ללא'}
מסר חינוכי (Moral Lesson): {user_input.moral_lesson}
נושאים להימנע מהם (Topics to Avoid): {user_input.topics_to_avoid or 'ללא'}
לכלול עובדה מעניינת (Include Fun Fact): {'כן' if user_input.include_fun_fact else 'לא'}

Create search queries that will help write a bedtime story with ALL these elements.
Research content appropriate for a {user_input.age}-year-old child.
"""
        result = await Runner.run(planner_agent, input_text)
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(StorySearchPlan)

    async def perform_searches(self, search_plan: StorySearchPlan) -> list[str]:
        """Perform all searches in parallel"""
        print("Searching for inspiration...")
        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
        print(f"Completed {len(results)} searches")
        return results

    async def search(self, item: StorySearchItem) -> str | None:
        """Perform a single search"""
        input_text = f"Search term: {item.query}\nPurpose: {item.purpose}"
        try:
            result = await Runner.run(research_agent, input_text)
            return str(result.final_output)
        except Exception as e:
            print(f"Search failed: {e}")
            return None

    async def write_story(
        self,
        user_input: UserInput,
        research_results: list[str],
    ) -> BedtimeStory:
        """Write the bedtime story"""
        print("Writing story...")

        input_text = f"Write a single bedtime story with the following parameters:\
            user's input: {user_input},\
            research_results: {research_results}"
        result = await Runner.run(writer_agent, input_text)
        print("Story draft complete")
        return result.final_output_as(BedtimeStory)

    async def evaluate_story(
        self, story: BedtimeStory, user_input: UserInput
    ) -> StoryEvaluation:
        """Evaluate the story for safety and quality"""
        print("Evaluating story...")
        input_text = f"Write a single bedtime story with the following parameters:\
            user's input: {user_input},\
            story: {story}"

        result = await Runner.run(guardian_agent, input_text)
        evaluation = result.final_output_as(StoryEvaluation)
        print(
            f"Evaluation: {'APPROVED' if evaluation.is_approved else 'NEEDS REVISION'}"
        )
        return evaluation

    async def revise_story(
        self,
        story: BedtimeStory,
        evaluation: StoryEvaluation,
        user_input: UserInput,
        research_results: list[str],
    ) -> BedtimeStory:
        """Revise the story based on Guardian feedback"""
        print("Revising story...")

        input_text = f"Revise this bedtime story with the following parameters:\
            user's input: {user_input},\
            research_results: {research_results},\
            previous_story: {story},\
            issues_to_fix: {evaluation.issues_found},\
            fix_instructions: {evaluation.fix_instructions}"
        result = await Runner.run(writer_agent, input_text)
        print("Revision complete")
        return result.final_output_as(BedtimeStory)
