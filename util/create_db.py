
# import sqlite3
# import pandas as pd
# import os

# ### This only needed to be run once to create the database

# def create_db():
    
#     df_billboard_200 = pd.read_csv("input_datasets/billboard200.csv")
#     df_billboard_100 = pd.read_csv("input_datasets/hot100.csv")
#     df_word_stats = pd.read_csv("input_datasets/word_ratings.csv")
    
    
#     conn = sqlite3.connect("billboard_data_and_word_list_data.db")
#     c = conn.cursor()
    
    
#     # c.execute('''CREATE TABLE IF NOT EXISTS billboard_hot_100 (
#     #                 Date TEXT,
#     #                 Song TEXT,
#     #                 Artist TEXT,
#     #                 Rank INTEGER,
#     #                 Last_Week INTEGER,
#     #                 Peak_Position INTEGER,
#     #                 Weeks_in_Charts INTEGER,
#     #                 Image_URL TEXT
#     #             )''')
    
#     # c.execute('''CREATE TABLE IF NOT EXISTS billboard_200 (
#     #                 Date TEXT,
#     #                 Song TEXT,
#     #                 Artist TEXT,
#     #                 Rank INTEGER,
#     #                 Last_Week INTEGER,
#     #                 Peak_Position INTEGER,
#     #                 Weeks_in_Charts INTEGER,
#     #                 Image_URL TEXT
#     #             )''')
    
#     c.execute('''CREATE TABLE IF NOT EXISTS word_stats (
#                     Word TEXT,
#                     V_Mean_Sum REAL,
#                     A_Mean_Sum REAL,
#                     D_Mean_Sum REAL )''')
#     # c.execute('''DROP TABLE IF EXISTS billboard_hot_100''')
#     # c.execute('''DROP TABLE IF EXISTS billboard_200''')
#     # c.execute('''DROP TABLE IF EXISTS word_stats''') # df_billboard_100.to_sql("billboard_hot_100", conn, if_exists="replace", index=False)
#     # df_billboard_200.to_sql("billboard_200", conn, if_exists="replace", index=False)
#     df_word_stats.to_sql("word_stats", conn, if_exists="replace", index=False)
    
#     conn.close()

# def main():
#     create_db()
    

# if __name__ == "__main__":
#     main()
