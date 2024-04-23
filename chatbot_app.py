import streamlit as st
from transformers import pipeline, set_seed
import requests



def fetch_image_url(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    

    
    params = {
        "q": query,
        "num": 1,
        "start": 1,
        "imgSize": "medium",
        "searchType": "image",
        "key": ###put your API key here,
        "cx": "e492d4ddd15f2480e",
    }
    
    
    response = requests.get(search_url, params=params)
    
    
    if response.status_code == 200:
        
        search_items = response.json().get("items")
        if not search_items:
            st.error("No results found.")
            return None
        image_url = search_items[0]["link"]
        return image_url
    else:
        st.error(f"Error during Google Image Search: {response.status_code}")
        st.error(f"Response Content: {response.text}")
        return None

set_seed(42)


story_generator = pipeline('text-generation', model='gpt2')


st.title('Story and Image Generation Studio')
st.write('Welcome! Enter a topic and let the AI craft a unique story and corresponding image for you.')


user_prompt = st.text_input('Enter your story prompt:', 'Once upon a time in a faraway kingdom...')


generate_button = st.button('Generate Story and Image')


story_placeholder = st.empty()
image_placeholder = st.empty()


if generate_button and user_prompt:
    
    with st.spinner('🤖 AI is crafting your story...'):
        generated_story = story_generator(user_prompt, max_length=200, num_return_sequences=1)
    story_placeholder.text_area('Generated Story:', generated_story[0]['generated_text'], height=300)
    
   
    with st.spinner('🎨 AI is finding your image...'):
        image_url = fetch_image_url(user_prompt)
        if image_url:
            image_placeholder.image(image_url, caption='Generated Image', use_column_width=True)
        else:
            st.error("Failed to retrieve an image.")
else:
    
    story_placeholder.text('Your generated story and image will appear here after you submit a prompt and press the button.')

