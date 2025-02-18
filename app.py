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

pp = pprint.PrettyPrinter(4, compact=True)


def load_json_files(directory):
    """Load all JSON files from a directory and return a list of their contents, starting from the 100th file and descending."""
    json_data = []
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return json_data
    
    # Get all JSON files in directory
    json_files = sorted(
        [f for f in os.listdir(directory) if f.endswith('.json')],
        key=lambda x: int(x.split('_')[-1].split('.')[0]),  # Sort numerically by chunk number
        reverse=True  # Sort in descending order
    )

    # Start from the 100th file
    json_files = json_files[99:]

    for file in json_files:
        file_path = os.path.join(directory, file)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                json_data.extend(data)  # Merge all song lists into one
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")
        except Exception as e:
            print(f"Unexpected error reading {file_path}: {e}")
    
    return json_data


def main():
    # Create directories if needed
    os.makedirs("test_datasets/1_27_25", exist_ok=True)

    # Define custom theme for rich console output
    custom_theme = Theme({
        "repr.number": "white",
        "valence": "#FFE5B4",
        "arousal": "#7DF9FF"
    })

    client = GenerateChatGPTDescriptions()
    console = Console(theme=custom_theme)

    # Display welcome message
    console.print("""Welcome to the Billboard Chart Annotator.\n
    This application queries ChatGPT to gather pseudo-emotional values ([valence]valence[/valence], [arousal]arousal[/arousal]) 
    for songs on the Billboard Hot 100 and Billboard 200 charts.""")

    console.print("""       
        - Method 1: Direct Estimate**  
        ChatGPT provides subjective [arousal]arousal[/arousal] and [valence]valence[/valence] scores (0 to 1) for each song.

        - Method 2: Descriptive Words**  
        ChatGPT generates five descriptive words for each song, which are mapped to [arousal]arousal[/arousal] and [valence]valence[/valence] 
          scores using the XANEW dataset. The scores are averaged for emotional estimation.

        - Method 3: Long-form Description**  
        ChatGPT creates a detailed emotional description of each song. Key words from the description are matched to XANEW scores, 
          and the averages are used to determine emotional attributes.
    """)

    console.print("Making test queries...")

    # Initialize last processed ID
    last_processed_id = None

    # Read processed data to find the last processed song
    try:
        with open("test_datasets/test_bb_processed.json", "r") as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    processed_entry = json.loads(line.rstrip(',\n'))
                    if processed_entry.get("processed"):
                        last_processed_id = processed_entry.get("id")
    except FileNotFoundError:
        console.print("[red]Processed file not found. Starting fresh.[/red]")

    # Ensure last_processed_id is defined
    if last_processed_id is None:
        console.print("No processed ID found. Starting from the beginning.")
    else:
        console.print(f"Last processed ID: {last_processed_id}")

    # Load all JSON files from split_files directory
    test_data = load_json_files("test_datasets/split_files")

    if not test_data:
        console.print("[red]No song data found. Exiting.[/red]")
        return

    # Initialize processing state
    start_processing = last_processed_id is None  # Start immediately if no ID was found
    song_list = []

    for song in test_data:
        if song.get("id") == last_processed_id:
            start_processing = True
            continue  # Skip the last processed song

        if start_processing:
            console.print(f"Processing song: {song.get('Song')} by {song.get('Artist')}")

            song_data = {
                "prompts": [],
                "song_name": song.get("Song"),
                "artist_name": song.get("Artist"),
                "date": song.get("Date")
            }

            # Generate prompts for annotation
            direct_estimation_prompt = Prompts.build_method_one_direct_estimation_prompt(song_data["song_name"], song_data["artist_name"])
            five_word_description_prompt = Prompts.build_method_two_5_word_descriptions(song_data["song_name"], song_data["artist_name"])
            long_form_description_prompt = Prompts.build_method_three_long_form_description_prompt(song_data["song_name"], song_data["artist_name"])

            prompts = [direct_estimation_prompt, five_word_description_prompt, long_form_description_prompt]

            # Get responses from ChatGPT
            annotated_response = []
            for prompt in prompts:
                try:
                    response = client.generate_chatgpt_response(prompt)
                    annotated_response.append(response)
                except openai.APIConnectionError:
                    console.print("[red]Rate limit exceeded. Retrying in 20 seconds...[/red]")
                    time.sleep(20)
                    response = client.generate_chatgpt_response(prompt)
                except openai.APIError as e:
                    console.print(f"[red]OpenAI API Error: {e}[/red]")
                    return None
                except openai.APITimeoutError as e:
                    console.print(f"[red]OpenAI API Timeout: {e}[/red]")
                    return None
                except Exception as e:
                    console.print(f"[red]An unexpected error occurred: {e}[/red]")
                    return None

            # Mark song as processed
            song.update({"processed": True})

            processed_id = {"id": song.get("id"), "processed": song.get("processed")}

            # Append processed song data to file
            with open('test_datasets/test_bb_processed.json', 'a') as f:
                json.dump(processed_id, f)
                f.write(',\n')

            # Build song data object
            song_data["prompts"] = annotated_response
            song_data["id"] = song.get("id")

            song_list.append(song_data)
            # pp.pprint(song_list)
            console.print(f"[green]Song processed: {song}[/green]")

            # Optional: Save song_list as batched JSON
            # Save the song list to a single JSON file
            with open('test_datasets/song_list_test_run.json', 'a') as outfile:
                    json.dump(song_data, outfile, indent=4)
                    outfile.write(',\n')
            
            # client.write_batched_json(song_list, 11, "test_datasets/test_run_2_10/", "hot100_batch_test_")  


if __name__ == "__main__":
    main()
