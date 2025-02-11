#!/usr/bin/env python3
import json
import os
import pprint
import time
import openai
from rich.console import Console
from rich.theme import Theme
from util.generate_chat_gpt_descriptions import GenerateChatGPTDescriptions
import util.prompts as Prompts

pp = pprint.PrettyPrinter(4,compact=True) 

def main():
    # init theme
    os.makedirs("test_datasets/1_27_25", exist_ok=True)
    custom_theme = Theme({
        "repr.number": "white",
        "valence": "#FFE5B4",
        "arousal": "#7DF9FF"
        })
    
    client = GenerateChatGPTDescriptions()
    console = Console(theme=custom_theme)   
    
    # TODO: put prompts in a separate file/greeting/logging/info tbd...
    console.print("""Welcome to the Billboard Chart Annotator.\n
    This application queries ChatGPT to gather pseudo-emotional values ([valence]valence[/valence], [arousal]arousal[/arousal]) for songs on the Billboard Hot 100 and Billboard 200 charts.""")
    console.print("""       
        - Method 1: Direct Estimate**  
        ChatGPT provides subjective [arousal]arousal[/arousal] and [valence]valence[/valence] scores (0 to 1) for each song.

        - Method 2: Descriptive Words**  
        ChatGPT generates five descriptive words for each song, which are mapped to [arousal]arousal[/arousal] and [valence]valence[/valence] scores using the XANEW dataset. The scores are averaged for emotional estimation.

        - Method 3: Long-form Description**  
        ChatGPT creates a detailed emotional description of each song. Key words from the description are matched to XANEW scores, and the averages are used to determine emotional attributes.
                  """
                  )
    console.print("Making test queries...")
    
<<<<<<< Updated upstream
=======
    # init the datasets to be loaded, needs to have flag that determines if it has been a annotated or not

    with open("test_datasets/test_bb_processed.json", "r") as f:
        for line in f:
            if line.strip():  # skip empty lines
                processed_entry = json.loads(line.rstrip(',\n'))
                if processed_entry.get("processed"):
                    last_processed_id = processed_entry.get("id")

    
    print(f"Last processed ID: {last_processed_id}")
        
>>>>>>> Stashed changes
    with open('test_datasets/test_bb.json', 'r') as f:
        test_data = json.load(f)

    # iterate through the songs, annotate, build objects, add array, write to file
    song_list = [] 
    start_processing = False
    for song in test_data:
        if song.get("id") == last_processed_id:
            start_processing = True
            continue  # skip the last processed song

        if start_processing:
            print(f"starting from: {song.get('id')}")
    
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
            
            # get prompts from GPT
            annotated_response = []
            for prompt in prompts:
                try:
                    response = client.generate_chatgpt_response(prompt)
                    annotated_response.append(response)
                except openai.APIConnectionError:
                    print("Rate limit exceeded. Retrying in 20 seconds...")
                    time.sleep(20)
                    response = client.generate_chatgpt_response(prompt)
                except openai.APIError as e:
                    print(f"OpenAI API Error: {e}")
                    return None
                except openai.APITimeoutError as e:
                    print(f"OpenAI API Error: {e}")
                    return None
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    return None
            
            # TODO: 
            song.update({"processed": True})
            
            processed_id = {}
            processed_id["id"] = song.get("id")
            processed_id["processed"] = song.get("processed")
            
            # write this dictionary to a file
            with open('test_datasets/test_bb_processed.json', 'a') as f:
                json.dump(processed_id, f)
                f.write(',\n')
                    
            # build song_data object
            song_data["prompts"] = annotated_response
            song_data["song_name"] = song_name
            song_data["artist_name"] = artist_name
            song_data["date"] = song.get("Date")
            song_data["id"] = song.get("id")
            
            
            
            song_list.append(song_data)
            pp.pprint(song_list)
            pp.pprint(f"song processed: {song}")
            
            print("test_data is: ")
            pp.pprint(type(test_data))
            pp.pprint(len(test_data))
            print(test_data)

        
        # convert song_list to JSON and write to file
        # client.write_batched_json(song_list, 11, "test_datasets/1_27_25/", "hot100_batch_test_5")     
        

if __name__ == "__main__":
    main()