import streamlit as st

# Simple story data structure: nodes with text, image, and choices
story = {
    "start": {
        "text": "You arrive at your new school on the first day. Suddenly, you notice a girl looking your way.",
        "image": "https://i.imgur.com/z7wWbWz.png",  # placeholder anime-style image URL
        "choices": {
            "Approach her": "meet_sakura",
            "Ignore and head to class": "ignore_girl"
        }
    },
    "meet_sakura": {
        "text": "She smiles shyly. \"Hi, I'm Sakura! Nice to meet you!\"",
        "image": "https://i.imgur.com/GR6VqTQ.png",
        "choices": {
            "Say hi back": "sakura_friend",
            "Be shy and walk away": "awkward_exit"
        }
    },
    "ignore_girl": {
        "text": "You decide not to talk and head straight to your classroom. But you can't help feeling like you missed something.",
        "image": "https://i.imgur.com/2ZC4Oa0.png",
        "choices": {
            "Go back and talk to her": "meet_sakura",
            "Stay in class": "classroom_scene"
        }
    },
    "sakura_friend": {
        "text": "You start chatting with Sakura and quickly become friends. She invites you to join the school ninja club!",
        "image": "https://i.imgur.com/0Jh0gRB.png",
        "choices": {
            "Join the ninja club": "ninja_club",
            "Politely decline": "decline_club"
        }
    },
    "awkward_exit": {
        "text": "You walk away awkwardly, feeling like you blew your chance.",
        "image": "https://i.imgur.com/fZDc88X.png",
        "choices": {
            "Try to apologize": "meet_sakura",
            "Ignore it and move on": "classroom_scene"
        }
    },
    "classroom_scene": {
        "text": "The class begins, but you keep thinking about the girl you ignored.",
        "image": "https://i.imgur.com/YPzXQjv.png",
        "choices": {
            "Daydream about ninja adventures": "ninja_daydream",
            "Focus on the class": "end"
        }
    },
    "ninja_club": {
        "text": "You join the ninja club! Exciting adventures await you and your new friends.",
        "image": "https://i.imgur.com/sXKWj2N.png",
        "choices": {
            "Start training": "end",
            "Ask about club secrets": "end"
        }
    },
    "decline_club": {
        "text": "You decline politely but promise to think about it. Sakura seems a little disappointed.",
        "image": "https://i.imgur.com/GR6VqTQ.png",
        "choices": {
            "Change your mind and join": "ninja_club",
            "Stick to your decision": "end"
        }
    },
    "ninja_daydream": {
        "text": "You imagine sneaking around the school at night, uncovering mysteries with your ninja skills.",
        "image": "https://i.imgur.com/RYnqS8J.png",
        "choices": {
            "Snap back to reality": "classroom_scene",
            "Keep daydreaming": "end"
        }
    },
    "end": {
        "text": "To be continued... Thanks for playing!",
        "image": "https://i.imgur.com/vZxPyXh.png",
        "choices": {}
    }
}

# Initialize story state
if "story_node" not in st.session_state:
    st.session_state.story_node = "start"

def render_node(node_key):
    node = story[node_key]
    st.image(node["image"], width=400)
    st.write(node["text"])

    if node["choices"]:
        choice = st.radio("Choose an option:", list(node["choices"].keys()), key=node_key)
        if st.button("Next"):
            st.session_state.story_node = node["choices"][choice]
            st.rerun()
    else:
        st.write("**The End**")
        if st.button("Restart"):
            st.session_state.story_node = "start"
            st.rerun()

# Page title
st.title("Ninja School Visual Novel - Inspired RPG")

# Render current story node
render_node(st.session_state.story_node)