import streamlit as st
import requests
from typing import Dict
from datetime import datetime

class MedViewChat:
    def __init__(self):
        self.initialize_session_state()
        self.setup_page_config()
        self.API_URL = "https://flowise-arvh.onrender.com/api/v1/prediction/d795c5af-396a-46f2-a707-446e36667f1d"
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Hello! I'm your MedView assistant. How can I help you with your medical device today?"
            }]
        if "category" not in st.session_state:
            st.session_state.category = "General"

    def setup_page_config(self):
        """Configure the Streamlit page"""
        st.set_page_config(
            page_title="MedView Assistant",
            page_icon="💬",
            layout="wide"
        )
        
    @staticmethod
    def get_category_descriptions() -> Dict[str, str]:
        """Return category descriptions"""
        return {
            "Setup & Sensor Placement": "Questions about device setup, sensor placement, and installation.",
            "Calibration & Device Connection": "Questions about calibration and pairing your device.",
            "Understanding Readings & Alerts": "Questions on interpreting device readings and alerts.",
            "Daily Usage & Data Management": "Questions regarding daily use, data review, and sharing device info.",
            "Maintenance & Sensor Replacement": "Questions about cleaning, maintaining, and replacing sensors.",
            "Troubleshooting & Common Issues": "Questions related to error messages and device troubleshooting.",
            "Travel & Storage": "Questions about storing supplies or traveling with your device."
        }

    def query(self, payload: Dict) -> Dict:
        """Send query to API and return JSON response"""
        try:
            response = requests.post(self.API_URL, json=payload)
            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return {"error": "Failed to get response from API"}

    def get_bot_response(self, question: str, category: str) -> str:
        """Get response from custom API"""
        try:
            payload = {
                "question": question,
                "category": category
            }
            
            with st.spinner("Thinking..."):
                response = self.query(payload)
                
                if "error" in response:
                    return "I apologize, but I'm having trouble connecting. Please try again."
                    
                return response.get("text", response)  # Handle both text and raw response formats
                
        except Exception as e:
            return "I apologize, but I encountered an error. Please try again in a moment."

    def render_sidebar(self):
        """Render sidebar with category selection"""
        with st.sidebar:
            st.image("https://placehold.co/600x200", caption="MedView Assistant")
            
            st.markdown("---")
            
            # Category selection
            st.header("Topic Selection")
            category = st.radio(
                "Choose a topic for your question:",
                list(self.get_category_descriptions().keys())
            )
            
            # Show category description
            if category:
                st.markdown("---")
                st.markdown(f"**About this topic:**")
                st.markdown(self.get_category_descriptions()[category])
            
            # Settings section
            with st.expander("⚙️ Settings"):
                st.selectbox("Theme:", ["Light", "Dark"], key="theme")
                st.slider("Chat Size", min_value=12, max_value=16, value=14, key="font_size")
            
            return category

    def render_chat_interface(self):
        """Render the main chat interface"""
        st.title("💬 MedView Assistant")
        st.caption("Your personal medical device support assistant")
        
        # Display chat messages
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # Get and display assistant response
            response = self.get_bot_response(prompt, st.session_state.category)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

    def run(self):
        """Run the Streamlit application"""
        # Render sidebar and get category
        category = self.render_sidebar()
        st.session_state.category = category
        
        # Render main chat interface
        self.render_chat_interface()

if __name__ == "__main__":
    app = MedViewChat()
    app.run()
