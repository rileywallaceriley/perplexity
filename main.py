import streamlit as st
import requests
import openai

# Retrieve API keys from Streamlit's secrets
PERPLEXITY_API_KEY = st.secrets["PERPLEXITY_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

def fetch_content_from_perplexity(topic, content_type, num_results):
    """
    Fetch content from Perplexity based on topic, content type, and number of results.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-7b-instruct",  # Adjust based on your requirement
        "messages": [
            {"role": "system", "content": f"Provide {num_results} latest {content_type} on {topic}."},
            {"role": "user", "content": topic}
        ],
        "max_tokens": 1024,  # Adjust as necessary
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from Perplexity API.")
        return []

def process_content_with_openai(content, desired_length):
    """
    Use OpenAI to process and improve the content for readability and length.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the latest available engine
            prompt=f"Summarize and enhance the following content for user-friendly reading, targeting a length of {desired_length} words:\n\n{content}",
            temperature=0.7,
            max_tokens=desired_length * 5,  # Estimate tokens based on desired word count
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Failed to process content with OpenAI: {str(e)}")
        return ""

def main():
    st.title("Enhanced Content Generator")

    topic = st.text_input("Topic Prompt", "")
    content_type = st.selectbox("Content Type", ["current news within 48 hours", "blog posts", "research articles"])
    num_results = st.number_input("Number of Results", min_value=1, max_value=5, value=3)
    desired_length = st.number_input("Desired Length (in words)", min_value=100, max_value=1000, value=200)
    
    if st.button("Generate"):
        if not topic:
            st.warning("Please insert a topic prompt.")
        else:
            raw_content = fetch_content_from_perplexity(topic, content_type, num_results)
            if raw_content:
                for content in raw_content.get('choices', []):
                    processed_content = process_content_with_openai(content.get('message', {}).get('content', ''), desired_length)
                    st.write(processed_content)
            else:
                st.write("No results found.")

if __name__ == "__main__":
    main()
