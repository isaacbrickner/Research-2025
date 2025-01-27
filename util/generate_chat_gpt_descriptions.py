import json
import os
from dotenv import load_dotenv
from openai import OpenAI


class GenerateChatGPTDescriptions:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    def __init__(self, billboard_chart=None, api_key=api_key):
        """
        Initializes the instance with the given billboard chart and API key.
        Args:
            billboard_chart (str, optional): The name of the billboard chart. Defaults to None.
            api_key (str): The API key for accessing the OpenAI service.
        """
        
        self.billboard_chart = billboard_chart
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        
    def generate_chatgpt_response(self, prompt):
        """
        Generates a response from the ChatGPT model based on the given prompt.
        Args:
            prompt (str): The input prompt to generate a response for.
        Returns:
            dict: The deserialized response from the ChatGPT model.
        Raises:
            Exception: If there is an error during the API call.
        """
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
        """
        Deserialize a JSON formatted string response.
        Args:
            response (str): A JSON formatted string.
        Returns:
            dict: A dictionary representation of the JSON string.
        """
        
        return json.loads(response)


    def write_batched_json(song_list, batch_size, output_directory, output_prefix):
        """
        Write a list of items to multiple JSON files in batches.

        :param song_list: List of items to write
        :param batch_size: Number of items per batch
        :param output_directory: Directory to save the files
        :param output_prefix: Prefix for output file names
        """
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        for i in range(0, len(song_list), batch_size):
            batch = song_list[i:i + batch_size]
            file_name = os.path.join(output_directory, f"{output_prefix}_batch_{i // batch_size + 1}.json")
            with open(file_name, 'w') as f:
                json.dump(batch, f, indent=4)
            print(f"Written batch {i // batch_size + 1} to {file_name}")