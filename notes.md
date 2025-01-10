Method 1: Direct Estimate
Prompt:
"Based on your subjective understanding of music, estimate the emotional valence (positivity/negativity) and arousal (intensity/energy) for the song titled '{song_title}' by {artist_name}. Provide your estimate as two numbers between 0 and 1: one for valence and one for arousal. Use this format: Valence: X.XX, Arousal: X.XX."

Method 2: Descriptive Words
Prompt:
"Provide five descriptive words that capture the emotional tone and mood of the song titled '{song_title}' by {artist_name}. Focus on words that reflect the song's emotional qualities. Please avoid repeating similar words."

Method 3: Long-Form Description
Prompt:
"Describe the emotional content and mood of the song titled '{song_title}' by {artist_name} in detail. Include observations about the overall tone, energy, and emotional atmosphere conveyed by the song. Aim to provide a paragraph that can be used to infer emotional valence (positivity/negativity) and arousal (intensity/energy)."

Method 1: Direct Estimate
Prompt:
"Based on your subjective understanding of music, estimate the emotional valence (positivity/negativity) and arousal (intensity/energy) for the song titled '{song_title}' by {artist_name}. Use the XANEW dataset of words as a reference for emotional attributes. Provide your estimate as two numbers between 0 and 1: one for valence and one for arousal. Use this format: Valence: X.XX, Arousal: X.XX."

Method 2: Descriptive Words
Prompt:
"Provide five descriptive words from the XANEW dataset that best capture the emotional tone and mood of the song titled '{song_title}' by {artist_name}. Ensure the words reflect the song's emotional qualities and are distinct from one another."

Method 3: Long-Form Description
Prompt:
"Describe the emotional content and mood of the song titled '{song_title}' by {artist_name} in detail. Use the XANEW dataset as a reference for selecting emotionally descriptive words. Include observations about the tone, energy, and emotional atmosphere conveyed by the song. Aim to provide a detailed description that incorporates words from the XANEW dataset, which can be used to infer emotional valence (positivity/negativity) and arousal (intensity/energy)."



import openai



# Load your OpenAI API key

openai.api_key = "YOUR_API_KEY"



# Read the file content

with open("my_document.pdf", "rb") as f:

    file_content = f.read()



# Upload the file

response = openai.File.create( 

    file=file_content,

    purpose="reference"  # Specify purpose as "reference" 

)



# Get the file ID

file_id = response["id"]



# Send a query referencing the uploaded file

response = openai.ChatCompletion.create(

    model="gpt-3.5-turbo",

    messages=[

        "Summarize the key points from the document: ",

        {"text": "Please refer to the file uploaded as 'my_document.pdf' ",

         "name": "user_file_reference"}

    ],

    "openaiFileIdRefs": [file_id] 

)



print(response["choices"][0]["text"])
