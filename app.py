#!/usr/bin/env python3
import json
import os
import pprint
import sys
import time
from dotenv import load_dotenv
import openai
from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown
from openai import OpenAI
import prompts as Prompts

pp = pprint.PrettyPrinter(4,compact=True)

# Die For You, The Weeknd & Ariana Grande


class GenerateChatGPTDescriptions:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    def __init__(self, billboard_chart=None, api_key=api_key):
        self.billboard_chart = billboard_chart
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        
    def generate_chatgpt_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"{prompt}"}], 
                response_format={ "type": "json_object" }
                )
        except Exception as e:
            print(f"Error: {e}")
        
        return self.deserialize_response(response.choices[0].message.content)

    def deserialize_response(self, response):
        return json.loads(response)
    
    
    


def main():
    custom_theme = Theme({
        "repr.number": "white",
        "valence": "#FFE5B4",
        "arousal": "#7DF9FF"
        })
    
    client = GenerateChatGPTDescriptions()
    console = Console(theme=custom_theme)   
    
    # TODO: put prompts in a separate file
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
    
    
    with open('test_datasets/test_bb.json', 'r') as f:
        test_data = json.load(f)
    

    song_list = [] 
    for song in test_data:
        song_name = song.get("Song")
        artist_name = song.get("Artist")
        console.print(f"Processing song: {song_name} by {artist_name}")
        
        song_data = {
            "prompts": [],
            "song_name": song_name,
            "artist_name": artist_name,
            "date": song.get("Date")
        }
        
        direct_estimation_prompt = Prompts.build_method_one_direct_estimation_prompt(song_name, artist_name)
        five_word_description_prompt = Prompts.build_method_two_5_word_descriptions(song_name, artist_name)
        long_form_description_prompt = Prompts.build_method_three_long_form_description_prompt(song_name, artist_name)
        
        prompts = [direct_estimation_prompt, five_word_description_prompt, long_form_description_prompt]
        
        annotated_response = []
        for prompt in prompts:
            try:
                response = client.generate_chatgpt_response(prompt)
                annotated_response.append(response)
            except openai.error.RateLimitError:
                print("Rate limit exceeded. Retrying in 20 seconds...")
                time.sleep(20)
                response = client.generate_chatgpt_response(prompt)
            except openai.error.APIError as e:
                print(f"OpenAI API Error: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None
        
        song_data["prompts"] = annotated_response
        song_data["song_name"] = song_name
        song_data["artist_name"] = artist_name
        song_data["date"] = song.get("Date")
        # pp.pprint(song_data)
        
        song_list.append(song_data)
        pp.pprint(song_list)
        
    
    # convert song_list to JSON and write to file
    with open('test_datasets/test.json', 'w') as f:
        json.dump(song_list, f, indent=4)          
            

if __name__ == "__main__":
    main()