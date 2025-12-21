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
):
    """Generate a bedtime story based on user input"""

    if not child_name:
        yield "נא להזין את שם הילד/ה!", ""
        return

    if not interests:
        yield "נא לבחור לפחות תחום עניין אחד!", ""
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
    title="DreamWeaver - סיפורי לילה טוב",
) as ui:

    gr.Markdown("# 🌙 DreamWeaver - סיפורי לילה טוב")

    # Row 1: Name, Age, Length
    with gr.Row():
        child_name = gr.Textbox(label="שם הילד/ה", placeholder="נועה", scale=2)
        age = gr.Slider(label="גיל", minimum=2, maximum=10, step=1, value=5, scale=1)
        story_length = gr.Radio(
            label="אורך הסיפור",
            choices=["short", "medium", "long"],
            value="medium",
            scale=1
        )

    # Row 2: Interests, Special Character, Moral
    with gr.Row():
        interests = gr.Dropdown(
            label="תחומי עניין (ניתן לבחור כמה)",
            choices=[
                "חיות", "חלל וכוכבים", "דינוזאורים", "נסיכות וטירות",
                "ים ויצורי ים", "קסם וקוסמים", "כלי רכב", "טבע ויערות",
                "גיבורי על", "פיות", "רובוטים", "מוזיקה", "ספורט", "בישול",
                "דרקונים", "חדי קרן", "פיראטים", "רכבות", "פרפרים", "גינות"
            ],
            multiselect=True,
            scale=2
        )
        special_character = gr.Textbox(
            label="דמות מיוחדת",
            placeholder="פלאפי החתול (אופציונלי)",
            scale=1
        )
        moral_lesson = gr.Dropdown(
            label="מסר חינוכי",
            choices=["ללא", "חסד ונתינה", "אומץ", "סקרנות", "סבלנות", "חברות", "להיות עצמך"],
            value="חסד ונתינה",
            scale=1
        )

    # Row 3: Avoid, Fun Fact
    with gr.Row():
        topics_to_avoid = gr.Textbox(
            label="נושאים להימנע מהם",
            placeholder="מים, כלבים (אופציונלי)",
            scale=2
        )
        include_fun_fact = gr.Checkbox(label="לכלול עובדה מעניינת", value=True, scale=1)

    # Full-width button
    generate_btn = gr.Button("✨ צור סיפור קסום", variant="primary", size="lg")

    # Status message (replaces itself)
    status_output = gr.Markdown(value="", elem_id="status")

    # Story output below
    story_output = gr.Markdown(value="", rtl=True)

    gr.Markdown(
        "🛡️ *כל סיפור נבדק על ידי שומר הסיפורים שלנו לבטיחות, תוכן מותאם גיל, וסיום מרגיע.*"
    )

    # Wire up the button
    generate_btn.click(
        fn=generate_story,
        inputs=[
            child_name, age, story_length, interests,
            special_character, moral_lesson, topics_to_avoid, include_fun_fact,
        ],
        outputs=[status_output, story_output],
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True)
