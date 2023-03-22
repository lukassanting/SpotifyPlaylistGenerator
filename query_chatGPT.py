import openai
import os


def generate_playlist_chatGPT():

    # get api key (make sure to follow steps in "commands_to_run" to get this to work)
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # inputs
    styles = input(
        "Give a list of songs / genres / artists to use a base (in the form 'Twenty One Pilots and ... and ...': ")
    number_of_songs = input("How many songs should the playlist contain? ")
    limit = input(
        "Should there be a limit to the number of songs similar to the prompt? (Y/N) ")
    if limit == "Y":
        limited_prompt = input("How many should it be limited to? ")

    # create prompt
    new_prompt = f"Create a playlist of at least 15 songs similar to {styles}"
    if limit == "Y":
        new_prompt = new_prompt + f", that does not contain more than 5 songs by them"
    new_prompt = new_prompt + ", and give it a title in the form 'Title: <title>'"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=new_prompt,
        temperature=0.6,
        max_tokens=int(number_of_songs) * 100
    )

    text_response = response.choices[0].text

    text_file = open("response.txt", "w")
    text_file.write(text_response)
    text_file.close()

    return text_response
