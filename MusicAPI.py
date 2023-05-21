import tkinter as tk
from tkinter import messagebox
import pip._vendor.requests as requests

def get_top_tracks():
    try:
        API_KEY = "e82a3eac1a45d908733a4dee786ac302"
        artist = artist_entry.get().title()
        artist = artist.replace(' ', '+')

        resp = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist}&api_key={API_KEY}&format=json"
        )
        toptrack = resp.json()

        song_list = []
        for song in toptrack["toptracks"]["track"]:
            song_list.append(song["name"])
        for i in range(len(song_list)):
            song_list[i] = song_list[i].replace(" ", "+")

        output_text.insert(tk.END, f'\nSongs sung by {artist.replace("+", " ")}:\n')
        output_text.insert(tk.END, '--------------' + ('-' * (len(artist) + 1)) + '\n')
        for i in song_list:
            output_text.insert(tk.END, f'{i.replace("+", " ")}\n')

        output_text.insert(tk.END, '\nSongs and their metadata:\n')
        output_text.insert(tk.END, '-------------------------\n')
        i = 1
        for song in song_list:
            resp = requests.get(
                f'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={API_KEY}&artist={artist}&track={song}&format=json'
            )
            song_data = resp.json()
            try:
                name = song.replace('+', ' ')
                release_date = song_data["track"]["wiki"]["published"]
                summary = song_data["track"]["wiki"]["summary"]
                url = song_data["track"]["url"]
                output_text.insert(tk.END, f'\n{i}) {name}, {artist.replace("+", " ")}, {release_date}\n\n')
                i += 1
                output_text.insert(tk.END, 'Song Trivia:\n------------\n')
                output_text.insert(tk.END, f'{summary}\n\n')
                output_text.insert(tk.END, 'Song URL:\n---------\n')
                output_text.insert(tk.END, f'{url}\n\n\n')
            except:
                output_text.insert(tk.END, f'No metadata found for {name}\n')
                continue
    except:
        messagebox.showerror("Error", "Artist Not Found")

root = tk.Tk()
root.title("Top Tracks")

artist_label = tk.Label(root, text="Enter Artist Name:")
artist_entry = tk.Entry(root)
submit_button = tk.Button(root, text="Submit", command=get_top_tracks)
output_text = tk.Text(root)

artist_label.pack()
artist_entry.pack()
submit_button.pack()
output_text.pack()

root.mainloop()
