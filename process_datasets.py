#!/usr/bin/env python3
import json
import os
import pprint
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown
from openai import OpenAI


pp = pprint.PrettyPrinter()

# Die For You, The Weeknd & Ariana Grande

def build_method_one_direct_estimation_prompt(song_name, artist_name):
    return f""""
        Based on your subjective understanding of music, estimate the emotional valence (positivity/negativity) and arousal (intensity/energy) for the song titled '{song_name}' by {artist_name}. Provide your estimate as two numbers between 0 and 1: one for valence and one for arousal. Use this format: Valence: X.XX, Arousal: X.XX.
        """

def build_method_two_5_word_descriptions(song_name, artist_name):
    return f""""
        Provide five descriptive words that capture the emotional tone and mood of the song titled '{song_name}' by {artist_name}. Focus on words that reflect the song's emotional qualities. Please avoid repeating similar words.
        """

def build_method_three_long_form_description_prompt(song_name, artist_name):
    return f"""
        Task:
        Analyze the song "{song_name}" by "{artist_name}" to identify the emotional content conveyed in the song. You can look at lyrics, analyses, reviews, interviews, fan discussions, and more. Based on your analysis, provide five descriptive words that accurately capture the song’s emotions.
        
        Output:
        Your output must be strictly in readable JSON format without any extra text:

        {{
        "words":
        [word1, word2, word3, word4, word5],
        "reasons":
            [reason for word1, reason for word2, reason for word3, reason for word4, reason for word5]
        }}

        Requirements:
        For the ‘outputs’ field, enter the words that accurately describe the emotional content of the song. No words should be repeated for the song. For the ‘reasons’ field, provide reasoning for each word separately. The reason for each word should be in the same order as the word.
        If you do not know the answer to a question, do not share false information. Instead, you should enter None for the ‘words’ and ‘reasons’ field.
"""

class GenerateChatGPTDescriptions:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    def __init__(self, billboard_chart=None, api_key=api_key):
        self.billboard_chart = billboard_chart
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        
    def generate_chatgpt_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"{prompt}"}],    
        )
        return self.deserialize_response(response.model_dump_json())

    def deserialize_response(self, response):
        return json.loads(response)

def main():
    custom_theme = Theme({
        "repr.number": "white",
        "valence": "#FFE5B4",
        "arousal": "#7DF9FF"
        })
    
    console = Console(theme=custom_theme)   
    
    console.print("""Welcome to the Billboard Chart Annotator.\n
    This application queries ChatGPT to gather pseudo-emotional values ([valence]valence[/valence], [arousal]arousal[/arousal]) for songs on the Billboard Hot 100 and Billboard 200 charts.""")
    console.print("""       
        - Method 1: Direct Estimate**  
        ChatGPT provides subjective [arousal]arousal[/arousal] and [valence]valence[/valence] scores (0 to 1) for each song.

        - Method 2: Descriptive Words**  
        ChatGPT generates five descriptive words for each song, which are mapped to [arousal]arousal[/arousal] and [valence]valence[/valence] scores using the XANEW dataset. The scores are averaged for emotional estimation.

        - Method 3: Long-form Description**  
        ChatGPT creates a detailed emotional description of each song. Key words from the description are matched to XANEW scores, and the averages are used to determine emotional attributes.
                  """)
    
    console.print("Making test queries...")
    
    client = GenerateChatGPTDescriptions()
    direct_estimation_prompt = build_method_one_direct_estimation_prompt("Die For You", "The Weeknd & Ariana Grande")
    five_word_description_prompt = build_method_two_5_word_descriptions("Die For You", "The Weeknd & Ariana Grande")
    long_form_description_prompt = build_method_three_long_form_description_prompt("Die For You", "The Weeknd & Ariana Grande")
    
    prompts = [direct_estimation_prompt, five_word_description_prompt, long_form_description_prompt]
    
    for prompt in prompts:
        response = client.generate_chatgpt_response(prompt)
        description = response["choices"][0]["message"]["content"]
        pp.pprint(description)
        print()
        print()
        print(type(description))
    

if __name__ == "__main__":
    main()