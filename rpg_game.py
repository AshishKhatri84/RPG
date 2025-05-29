import streamlit as st
import json
from openai import OpenAI

# Initialize OpenAI client with API key
# You can set OPENAI_API_KEY in environment or Streamlit secrets
api_key = st.secrets.get("OPENAI_API_KEY", "your-api-key-here")
client = OpenAI(api_key=api_key)

# Initialize session state variables if they don't exist
if 'character' not in st.session_state:
    st.session_state.character = {}
if 'stats' not in st.session_state:
    st.session_state.stats = {'health': 100, 'mana': 50, 'experience': 0}
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'story' not in st.session_state:
    st.session_state.story = []
if 'option_selected' not in st.session_state:
    st.session_state.option_selected = None

def save_game():
    save_data = {
        'character': st.session_state.character,
        'stats': st.session_state.stats,
        'inventory': st.session_state.inventory,
        'story': st.session_state.story
    }
    return json.dumps(save_data, indent=2)

def load_game(uploaded_file):
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        st.session_state.character = data.get('character', {})
        st.session_state.stats = data.get('stats', {'health': 100, 'mana': 50, 'experience': 0})
        st.session_state.inventory = data.get('inventory', [])
        st.session_state.story = data.get('story', [])
        st.session_state.option_selected = None
        st.success("Game loaded successfully!")

def continue_story(user_choice):
    if user_choice is not None:
        st.session_state.story.append({"role": "user", "content": f"I choose: {user_choice}"})

    conversation = [{"role": "system", "content": "You are the narrator of a fantasy RPG game. Make the story engaging, vivid, and interactive."}]
    conversation.extend(st.session_state.story)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.9,
    )

    story_text = response.choices[0].message.content
    st.session_state.story.append({"role": "assistant", "content": story_text})

    options = []
    lines = story_text.split('\n')
    for line in lines:
        if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            option = line.strip().split('.', 1)[1].strip()
            options.append(option)

    return options

def show_character_creation():
    st.header("🎭 Character Creation")
    if 'name' not in st.session_state.character:
        st.session_state.character['name'] = ''
    if 'class' not in st.session_state.character:
        st.session_state.character['class'] = 'Warrior'

    name = st.text_input("Enter your character's name:", st.session_state.character['name'])
    char_class = st.selectbox("Choose your class:", ["Warrior", "Mage", "Rogue"], index=["Warrior", "Mage", "Rogue"].index(st.session_state.character['class']))

    if st.button("Create Character"):
        if not name:
            st.error("Please enter a name for your character.")
            return False
        st.session_state.character['name'] = name
        st.session_state.character['class'] = char_class

        if char_class == "Warrior":
            st.session_state.stats = {'health': 150, 'mana': 20, 'experience': 0}
            st.session_state.inventory = ['Sword', 'Shield']
        elif char_class == "Mage":
            st.session_state.stats = {'health': 80, 'mana': 150, 'experience': 0}
            st.session_state.inventory = ['Staff', 'Spellbook']
        elif char_class == "Rogue":
            st.session_state.stats = {'health': 100, 'mana': 60, 'experience': 0}
            st.session_state.inventory = ['Daggers', 'Lockpick']

        st.session_state.story = []
        st.session_state.option_selected = None
        st.success(f"Character '{name}' the {char_class} created! Ready to start your adventure.")
        return True
    return False

def main():
    st.title("🛡️ Prompt RPG Game")

    st.sidebar.header("🧙‍♂️ Character Info")
    if st.session_state.character.get('name'):
        st.sidebar.write(f"**Name:** {st.session_state.character['name']}")
        st.sidebar.write(f"**Class:** {st.session_state.character['class']}")
    else:
        st.sidebar.write("No character created yet.")

    st.sidebar.write("### Stats")
    for stat, val in st.session_state.stats.items():
        st.sidebar.write(f"{stat.capitalize()}: {val}")

    st.sidebar.write("### Inventory")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.sidebar.write(f"• {item}")
    else:
        st.sidebar.write("Empty")

    st.sidebar.markdown("---")
    st.sidebar.header("💾 Save / Load Game")
    if st.sidebar.button("Save Game"):
        json_data = save_game()
        st.sidebar.download_button("Download Save File", data=json_data, file_name="rpg_save.json", mime="application/json")
    
    uploaded_file = st.sidebar.file_uploader("Upload Save File", type=["json"])
    if uploaded_file:
        load_game(uploaded_file)

    if not st.session_state.character.get('name'):
        created = show_character_creation()
        if not created:
            st.info("Please create your character to start the adventure.")
        return

    if st.button("Start New Game"):
        st.session_state.story = []
        st.session_state.option_selected = None
        intro_text = f"You are {st.session_state.character['name']}, a {st.session_state.character['class']} starting your adventure. Describe the first scene and present options."
        st.session_state.story.append({"role": "system", "content": intro_text})
        options = continue_story(None)
        st.session_state.options = options
    elif 'options' in st.session_state:
        options = st.session_state.options
    else:
        options = continue_story(None)
        st.session_state.options = options

    st.subheader("📜 Story So Far:")
    for entry in st.session_state.story:
        role = entry['role']
        content = entry['content']
        if role == 'user':
            st.markdown(f"**You:** {content[9:]}")
        else:
            st.markdown(f"**Narrator:** {content}")

    if options:
        st.subheader("🗡️ What do you do next?")
        choice = st.radio("Choose an option:", options, index=0)
        if st.button("Submit Choice"):
            st.session_state.option_selected = choice
            if "sword" in choice.lower() and "Sword" not in st.session_state.inventory:
                st.session_state.inventory.append("Sword")
                st.success("You obtained a Sword! ⚔️")
            if "potion" in choice.lower() and "Healing Potion" not in st.session_state.inventory:
                st.session_state.inventory.append("Healing Potion")
                st.success("You found a Healing Potion! 🧪")

            options = continue_story(choice)
            st.session_state.options = options
            st.experimental_rerun()
    else:
        st.info("No options available. The adventure might have ended or need a restart.")

if __name__ == "__main__":
    main()