

def build_method_one_direct_estimation_prompt(song_name, artist_name):
    return f""""
        Based on your subjective understanding of music, estimate the emotional valence (positivity/negativity) and arousal (intensity/energy) for the song titled '{song_name}' by {artist_name}. Provide your estimate as two numbers between 0 and 1: one for valence and one for arousal. Use this format: Valence: X.XX, Arousal: X.XX. Please structure this response in JSON format like 
        {{
            "valence": 0.7,
            "arousal": 0.4
        }}
        """

# def build_method_two_5_word_descriptions(song_name, artist_name):
#     return f""""
#         Provide five descriptive words that capture the emotional tone and mood of the song titled '{song_name}' by {artist_name}. Focus on words that reflect the song's emotional qualities. Please avoid repeating similar words. Please structure this response in JSON format.
#         {{
#             "words": ["happy", "joyful", "excited", "optimistic", "elated"]
#         }}   
        
#         """

def build_method_two_5_word_descriptions(song_name, artist_name):
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

def build_method_three_long_form_description_prompt(song_name, artist_name):
    return f"""
        Task:
        Analyze the song "{song_name}" by "{artist_name}". Your analysis should focus on the emotional content conveyed in the song. Examine elements like lyrics, melody, vocals, and instrumentation to identify the emotional depth and impact of the song. 
        
        Output:
        Your output must be strictly in readable JSON format without any extra text:

        {{
        "paragraph": "A detailed summary of the song's emotional themes, lyrical content, and musical arrangement.",
        "reasons": [
            "Reason 1: Explanation of how specific elements contribute to the emotions conveyed in the song.",
            "Reason 2: Explanation of another element's contribution to the emotional resonance.",
            "Reason 3: Further reasoning linked to a different aspect of the song.",
            "Reason 4: Additional reasoning focusing on instrumental or vocal performance.",
            "Reason 5: Any other aspect that enhances the song's emotional intensity."
        ]
        }}

        Requirements:
        - The 'paragraph' field must summarize the song's emotional essence based on the analysis.
        - The 'reasons' field must provide five specific explanations, each linked to a distinct contributing factor in the song.
        - Avoid repetition across the reasons and ensure clarity in each explanation.
        - If you do not know the answer to the task, do not generate false information. Instead, you should enter None for both the 'paragraph' and 'reasons' fields.
    """
