import streamlit as st


prompt1='''You are a skilled sales agent tasked with selling a high-performance laptop, the Vertex UltraBook 15X Pro, priced at $1,299. Your objective is to effectively communicate the product's features, address customer queries, and close the sale. Product Specifications: Display: 15.6" Full HD IPS (1920x1080) with anti-glare technology, Processor: Intel Core i7-13700H (13th Gen, up to 5.0 GHz), RAM: 16GB DDR5, Storage: 1TB NVMe SSD, Graphics: NVIDIA GeForce RTX 4060 (6GB GDDR6), Battery: Up to 10 hours (70Wh battery), Weight: 3.4 lbs (1.54 kg), Features: Backlit keyboard, fingerprint reader, Wi-Fi 6, Thunderbolt 4, Operating System: Windows 11 Pro. Your approach: Use the duckduckgo_search function for user queries requiring a web search. If the user shows interest in another product, use the query_product_db function to fetch details. If the user asks what products do you sell? use query_product_db function.  Do not call these functions more than three times. Engage customers, handle objections, and stick to the price of $1,299 unless offering a 10% discount to previous customers. Close the sale by collecting credit card details and end with a post-sale survey.'''





def main():
    # Page configuration
    st.set_page_config(
        page_title="AI Voice Assistant",
        page_icon="🎤",
        layout="wide"
    )

    # Text input for Customer ID and Prompt
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    st.header("🎤 Welcome to the AI Voice Assistant App")
    st.info("ℹ️ Please enter your CUSTOMER_ID to proceed.")

    customer_id = st.text_input("🔑 Enter CUSTOMER_ID (required):", key="customer_id")
    prompt = st.text_area("📝 Enter a prompt (optional):", key="prompt")

    # Save inputs to files
    if st.button("🚀 Submit"):
        if customer_id.strip() == "":
            st.error("❌ CUSTOMER_ID is required to proceed!")
        else:
            st.session_state.authenticated = True
            with open("customer_id.txt", "w") as f:
                f.write(customer_id.strip())
            if prompt.strip() != "":
                with open("prompt.py", "w") as f:
                    f.write(f"PROMPT='''\n{prompt.strip()}\n'''\n")
            else:
                with open("prompt.py", "w") as f:
                    f.write(f"PROMPT='''\n{prompt1}\n'''\n")
            st.success("✅ Details saved successfully!")

    # Display content only if authenticated
    if st.session_state.authenticated:
        # Main Application Page
        st.title("🎤 Welcome to Your AI Voice Assistant")
        
        # Introduction section
        st.header("ℹ️ About This Application")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            🗣️ Welcome to your personal AI Voice Assistant! This application allows you to:
            
            - 🤖 Have natural voice conversations with an AI assistant
            - 🔄 Get real-time responses to your questions
            - 🗂️ View your entire conversation history
            - 🤓 Interact with various AI models including Claude 3.5 Haiku
            
            To get started, click on the '🎤 Voice Chat' tab in the sidebar to begin your conversation!
            """)
            
            # Quick start guide
            st.subheader("🚀 Quick Start Guide")
            st.markdown("""
            1️⃣ Navigate to the 🎤 Voice Chat tab  
            2️⃣ Allow 🎙️ microphone access when prompted  
            3️⃣ Start speaking naturally with your assistant  
            4️⃣ View your conversation in real-time  
            """)
        
        with col2:
            # System Status
            st.subheader("⚙️ System Status")
            st.success("✅ System Online")
            st.info("🎙️ Microphone: Ready")
            st.info("🔊 Speaker: Ready")
            
            # Add a divider
            st.divider()
            
            # Version info
            st.caption("🆚 Current Version: 1.0.0")
            st.caption("🤖 Using Claude 3.5 Haiku")

        # Features section
        st.header("✨ Key Features")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.markdown("### 🗣️ Voice Recognition")
            st.markdown("🎧 High-accuracy speech recognition powered by Deepgram Nova-2")
        
        with col4:
            st.markdown("### 🤖 AI Processing")
            st.markdown("🧠 Advanced language processing using Claude 3.5 Haiku")
        
        with col5:
            st.markdown("### 🔊 Natural Speech")
            st.markdown("📢 High-quality voice synthesis using Aura Luna")

        # Footer section
        st.divider()
        st.markdown("""
        <div style='text-align: center'>
            <p>❤️ Made with Streamlit, Deepgram, and Anthropic Claude</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
