import streamlit as st
import requests
import json

# Initialize session state
if 'thread_ids' not in st.session_state:
    st.session_state.thread_ids = []
if 'messages' not in st.session_state:
    st.session_state.messages = {}
if 'file_b_conversation' not in st.session_state:
    st.session_state.file_b_conversation = []

st.set_page_config(layout="wide")

# Custom CSS for layout
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 40vh;
    justify-content: flex-end;
    margin-top: auto;
}
.conversation-container {
    flex-grow: 1;
    overflow-y: auto;
    padding-bottom: 10px;
}
.chat-interface {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: white;
    width: 50%;
    padding: 10px;
    border-top: 1px solid #e6e6e6;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Sidebar (narrow column)
with st.sidebar:
    st.header("Thread Management")
    
    # Input for new thread ID
    new_thread_id = st.text_input("Enter a new thread ID:")
    if st.button("Create New Thread"):
        if new_thread_id and new_thread_id not in st.session_state.thread_ids:
            st.session_state.thread_ids.append(new_thread_id)
            st.session_state.messages[new_thread_id] = []
            st.success(f"New thread '{new_thread_id}' created!")
        elif new_thread_id in st.session_state.thread_ids:
            st.warning("This thread ID already exists.")
        else:
            st.warning("Please enter a valid thread ID.")

    # Select existing thread
    selected_thread = st.selectbox("Select a thread:", st.session_state.thread_ids)

# Main content
st.title("Chatbot with Multiple Threads")

if selected_thread:
    with st.container():
        st.header(f"Conversation in Thread: {selected_thread}")
        # Display previous messages
        for message in st.session_state.messages[selected_thread]:
            if message['role'] == 'user':
                st.text_area("User", value=message['content'], height=100, disabled=True)
            else:
                st.text_area("ChatBot", value=message['content'], height=100, disabled=True)

    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # User input section fixed at bottom center
        st.markdown('<div class="chat-interface">', unsafe_allow_html=True)
        st.header("Chat Interface")
        
        # User input
        user_input = st.text_input("Your message:")

        if st.button("Send"):
            if user_input:
                # Send request to FastAPI backend
                response = requests.post("ttp://127.0.0.1:8080/api/rag/chat",
                                         json={"thread_id": selected_thread, "message": user_input})
                
                if response.status_code == 200:
                    bot_response = response.json()['response']
                    
                    # Update messages
                    st.session_state.messages[selected_thread].append({"role": "user", "content": user_input})
                    st.session_state.messages[selected_thread].append({"role": "bot", "content": bot_response})

                    # Update FILE-B conversation
                    st.session_state.file_b_conversation.append(f"Sent to FILE-B: {user_input}")
                    st.session_state.file_b_conversation.append(f"Received from FILE-B: {bot_response}")

                    # Clear input and rerun
                    st.experimental_rerun()
                else:
                    st.error("Failed to get response from the server.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="conversation-container">', unsafe_allow_html=True)
            st.header("Conversation with FILE-B")
            # Display conversation with FILE-B
            for message in st.session_state.file_b_conversation:
                st.text(message)

            # Add a clear button for FILE-B conversation
            if st.button("Clear FILE-B Conversation"):
                st.session_state.file_b_conversation = []
                st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("Please select a thread from the sidebar to view conversations.")