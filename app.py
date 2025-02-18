#!/usr/bin/env python3
import json
import os
import time
import openai
from rich.console import Console
from rich.theme import Theme
from util.generate_chat_gpt_descriptions import GenerateChatGPTDescriptions
import util.prompts as Prompts

def load_json_files(directory):
    """Load all JSON files from a directory and return a list of their contents."""
    json_data = []

    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return json_data
    
    json_files = sorted(
        [f for f in os.listdir(directory) if f.endswith('.json')],
        key=lambda x: int(x.split('_')[-1].split('.')[0]),  
        reverse=True  
    )

    for file in json_files:
        file_path = os.path.join(directory, file)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                json_data.extend(data)  
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")
        except Exception as e:
            print(f"Unexpected error reading {file_path}: {e}")
    
    return json_data

def load_processed_ids(file_path):
    """Load processed UUIDs from the tracking file."""
    processed_ids = set()
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line.strip():  
                    processed_entry = json.loads(line.rstrip(',\n'))
                    if processed_entry.get("processed"):
                        processed_ids.add(processed_entry.get("id"))
    except FileNotFoundError:
        print("[red]Processed file not found. Starting fresh.[/red]")
    return processed_ids

def contains_null_values(data):
    """Recursively check if any value in a dictionary or list is null."""
    if isinstance(data, dict):
        return any(contains_null_values(v) for v in data.values())
    if isinstance(data, list):
        return any(contains_null_values(item) for item in data)
    return data is None  # Base case: If the value itself is None

def main():
    os.makedirs("test_datasets/1_27_25", exist_ok=True)

    custom_theme = Theme({
        "repr.number": "white",
        "valence": "#FFE5B4",
        "arousal": "#7DF9FF"
    })

    client = GenerateChatGPTDescriptions()
    console = Console(theme=custom_theme)

    console.print("Making test queries...")

    processed_file = "test_datasets/test_bb_processed.json"
    processed_ids = load_processed_ids(processed_file)

    test_data = load_json_files("test_datasets/split_files")

    if not test_data:
        console.print("[red]No song data found. Exiting.[/red]")
        return

    for song in test_data:
        song_id = song.get("id")

        if song_id in processed_ids:
            console.print(f"[yellow]Skipping duplicate: {song.get('Song')} by {song.get('Artist')}[/yellow]")
            continue  

        console.print(f"Processing song: {song.get('Song')} by {song.get('Artist')}")

        song_data = {
            "prompts": [
                {
                    "valence": None,
                    "arousal": None
                },
                {
                    "words": None,
                    "reasons": None
                },
                {
                    "paragraph": None,
                    "reasons": [None, None, None, None, None]
                }
            ],
            "song_name": song.get("Song"),
            "artist_name": song.get("Artist"),
            "date": song.get("Date")
        }

        direct_estimation_prompt = Prompts.build_method_one_direct_estimation_prompt(song_data["song_name"], song_data["artist_name"])
        five_word_description_prompt = Prompts.build_method_two_5_word_descriptions(song_data["song_name"], song_data["artist_name"])
        long_form_description_prompt = Prompts.build_method_three_long_form_description_prompt(song_data["song_name"], song_data["artist_name"])

        prompts = [direct_estimation_prompt, five_word_description_prompt, long_form_description_prompt]

        for idx, prompt in enumerate(prompts):
            if not prompt:
                console.print(f"[red]Skipping empty prompt.[/red]")
                continue

            max_retries = 3
            attempt = 0
            response = None

            while attempt < max_retries:
                try:
                    response = client.generate_chatgpt_response(prompt)
                    
                    if response and not contains_null_values(response):  
                        break  # Exit loop if response is valid
                    else:
                        console.print(f"[yellow]Invalid response (null values found). Retrying ({attempt+1}/{max_retries}) after 5 seconds...[/yellow]")
                        time.sleep(5)  # Wait for 5 seconds before retrying

                except openai.APIConnectionError:
                    console.print("[red]Rate limit exceeded. Retrying in 20 seconds...[/red]")
                    time.sleep(20)

                except openai.APIError as e:
                    console.print(f"[red]OpenAI API Error: {e}[/red]")
                    break  # Stop retrying if it's an API error

                except openai.APITimeoutError as e:
                    console.print(f"[red]OpenAI API Timeout: {e}. Retrying in 5 seconds...[/red]")
                    time.sleep(5)

                except Exception as e:
                    console.print(f"[red]Unexpected error: {e}[/red]")
                    break  # Stop retrying if it's an unknown error

                attempt += 1

            # If response is valid, update the corresponding section
            if response and not contains_null_values(response):
                song_data["prompts"][idx] = response
            else:
                console.print(f"[yellow]Failed to get a valid response after {max_retries} retries. Keeping placeholders.[/yellow]")

        # Mark song as processed
        song.update({"processed": True})
        processed_entry = {"id": song_id, "processed": True}

        with open(processed_file, 'a') as f:
            json.dump(processed_entry, f)
            f.write(',\n')

        with open('test_datasets/song_list_test_run.json', 'a') as outfile:
            json.dump(song_data, outfile, indent=4)
            outfile.write(',\n')

        console.print(f"[green]Song processed: {song.get('Song')} by {song.get('Artist')}[/green]")

if __name__ == "__main__":
    main()
