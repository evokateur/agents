import gradio as gr
from dotenv import load_dotenv
from story_manager import StoryManager, UserInput

load_dotenv(override=True)


async def generate_story(
    child_name: str,
    age: int,
    story_length: str,
    interests: list[str],
    special_character: str,
    moral_lesson: str,
    topics_to_avoid: str,
    include_fun_fact: bool,
    story_language: str,
):
    """Generate a bedtime story based on user input"""

    if not child_name:
        yield "Please enter the child's name!", ""
        return

    if not interests:
        yield "Please select at least one interest!", ""
        return

    user_input = UserInput(
        child_name=child_name,
        age=age,
        story_length=story_length,
        interests=interests,
        special_character=special_character if special_character else None,
        moral_lesson=moral_lesson,
        topics_to_avoid=topics_to_avoid if topics_to_avoid else None,
        include_fun_fact=include_fun_fact,
        story_language=story_language,
    )

    async for chunk in StoryManager().run(user_input):
        # Check if this is the final story (starts with #)
        if chunk.startswith("# ") or chunk.startswith("---"):
            yield "", chunk  # Clear status, show story
        else:
            yield chunk, ""  # Show status, clear story


# Build the Gradio UI
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="purple", secondary_hue="pink"),
    title="DreamWeaver - Bedtime Stories",
) as ui:

    gr.Markdown("# 🌙 DreamWeaver - Bedtime Stories")

    # Row 1: Name, Age, Length
    with gr.Row():
        child_name = gr.Textbox(label="Child's Name", placeholder="Noa", scale=2)
        age = gr.Slider(label="Age", minimum=2, maximum=10, step=1, value=5, scale=1)
        story_length = gr.Radio(
            label="Story Length",
            choices=["short", "medium", "long"],
            value="medium",
            scale=1
        )

    # Row 2: Interests, Special Character, Moral
    with gr.Row():
        interests = gr.Dropdown(
            label="Interests (select multiple)",
            choices=[
                "Animals", "Space and Stars", "Dinosaurs", "Princesses and Castles",
                "Ocean and Sea Creatures", "Magic and Wizards", "Vehicles", "Nature and Forests",
                "Superheroes", "Fairies", "Robots", "Music", "Sports", "Cooking",
                "Dragons", "Unicorns", "Pirates", "Trains", "Butterflies", "Gardens"
            ],
            multiselect=True,
            scale=2
        )
        special_character = gr.Textbox(
            label="Special Character",
            placeholder="Fluffy the cat (optional)",
            scale=1
        )
        moral_lesson = gr.Dropdown(
            label="Moral Lesson",
            choices=["None", "Kindness and Giving", "Courage", "Curiosity", "Patience", "Friendship", "Being Yourself"],
            value="Kindness and Giving",
            scale=1
        )

    # Row 3: Avoid, Fun Fact, Language
    with gr.Row():
        topics_to_avoid = gr.Textbox(
            label="Topics to Avoid",
            placeholder="water, dogs (optional)",
            scale=2
        )
        include_fun_fact = gr.Checkbox(label="Include Fun Fact", value=True, scale=1)
        story_language = gr.Radio(
            label="Story Language",
            choices=["Hebrew", "English"],
            value="Hebrew",
            scale=1
        )

    # Full-width button
    generate_btn = gr.Button("✨ Create Magical Story", variant="primary", size="lg")

    # Status message (replaces itself)
    status_output = gr.Markdown(value="", elem_id="status")

    # Story output below
    story_output = gr.Markdown(value="", rtl=True)

    gr.Markdown(
        "🛡️ *Every story is reviewed by our Story Guardian for safety, age-appropriate content, and a calming ending.*"
    )

    # Wire up the button
    generate_btn.click(
        fn=generate_story,
        inputs=[
            child_name, age, story_length, interests,
            special_character, moral_lesson, topics_to_avoid, include_fun_fact,
            story_language,
        ],
        outputs=[status_output, story_output],
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True)
