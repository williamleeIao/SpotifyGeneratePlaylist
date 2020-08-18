from tkinter import Tk, RIGHT, BOTH, RAISED, X, N, LEFT, Text, IntVar, StringVar, BOTTOM, W, Listbox, END, Y, TOP, Menu, \
    DISABLED, NORMAL, Toplevel, CENTER
from tkinter.ttk import Frame, Button, Style, Label, Entry, Checkbutton, LabelFrame, Scrollbar, Radiobutton, Progressbar
from YouTube_Handler import YouTube_Operation
from Spotify_Handler import Spotify_Operation
from secrets import spotify_user_id
import json
import os


class UI(Frame):
    def __init__(self, root):
        super().__init__()
        self.youtube_op = YouTube_Operation()
        self.client = self.youtube_op.create_youtube_client()
        self.spotipy_client = Spotify_Operation()
        self.root = root
        self.initUI()

    def youtube_like_videos(self):
        self.youtube_op.get_liked_videos(self.client)

    def click_event_go(self):
        # cs = self.mylist.curselection()
        self.entry1.config(textvariable="ABC")

    def initUI(self):
        self.master.title("YouTube liked Videos to Spotify")
        self.pack(fill=BOTH, expand=False)

        # --------------button frame----------------------------
        frame1 = Frame(self)
        frame1.pack(fill=X)

        btn1 = Button(frame1, text=' Get like Video from youtube', width=30,
                      command=lambda: self.run()
                      )
        btn1.pack(side=TOP, padx=5, pady=5)

        # -------------list box----------------------------------
        frame2 = Frame(self)
        frame2.pack(fill=X)
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side=RIGHT, anchor=N, fill=Y, padx=5, pady=5)

        # Example
        self.mylist = Listbox(frame2, yscrollcommand=scrollbar.set)

        # for line in range(200):
        #     self.mylist.insert(END, "I am EMPTY, PLease don't surprise")

        scrollbar.config(command=self.mylist.yview)
        # -------------------Indicator show  for spotify playlist (currently one playlist)-----------------#

        frame3 = Frame(self)
        frame3.pack(fill=X)
        self.Title = StringVar()
        self.entry1 = Entry(frame3, textvariable=self.Title)
        self.entry1.pack(fill=X)
        self.entry1.config(textvariable="AAAAA")
        frame4 = Frame(self)
        frame4.pack(fill=X)

        btn2 = Button(frame4, text=' Import to Spotify Playlist', width=30,
                      command=lambda: self.add_into_spotipy_playlist()
                      )
        btn2.pack(side=TOP, padx=5, pady=5)

        #-------------------Indicator show  for spotify playlist (currently one playlist)-----------------#
        frame5 = Frame(self)
        frame5.pack(fill=X)

        scrollbar = Scrollbar(frame5)
        scrollbar.pack(side=RIGHT, anchor=N, fill=Y, padx=5, pady=5)

        # Example
        self.Spotifylist = Listbox(frame5, yscrollcommand=scrollbar.set)

        for line in range(200):
            self.Spotifylist.insert(END, "I am EMPTY, PLease don't surprise")

        scrollbar.config(command=self.Spotifylist.yview)

        # -------------------Indicator show  for spotify playlist (currently one playlist)-----------------#
        frame6 = Frame(self)
        frame6.pack(fill=X)

        btn1 = Button(frame6, text=' Show Playlist from spotify', width=30,
                      command=lambda: self.run()
                      )
        btn1.pack(side=TOP, padx=5, pady=5)

        self.mylist.bind('<<ListboxSelect>>', self.onselect)
        self.mylist.pack(side=LEFT, fill=BOTH, expand=True)
        self.master.bind("<FocusOut>", self.on_focus_out)

    def on_focus_out(self, ent):
        print(ent.widget)
        if ent.widget._w == '.!ui.!frame3.!entry':
            user_input = self.entry1.get()
            print(user_input)

    def add_into_spotipy_playlist(self):
        # need to refresh?
        self.entry1.get()
        print(self.entry1.get())
        song_id = self.spotipy_client.get_spotify_uri(self.entry1.get())
        playlist_id = self.spotipy_client.get_playlist_id(spotify_user_id)

        self.spotipy_client.add_song_to_playlist(
            song_id,
            playlist_id.split(':')[2] if 'playlist' in playlist_id else 'nothing'
        )

    def run(self):
        # load json file
        self.youtube_like_videos()
        current_path = os.getcwd()
        # create new file and save as json file
        song_title = current_path + "\\" + 'song_info.json'
        with open(song_title, "r") as inputfile:
            data = json.load(inputfile)
            for p in data['song_Info']:
                # show in the listbox
                print('song_title: {}'.format(p['song_title']))
                print('song_description: {} '.format(p['song_description']))
                print('song_tag: {}'.format(p['song_description']))
                self.mylist.insert(END, p['song_title'])

    def onselect(self, val):
        # Note here that Tkinter passes an event object to onselect()
        w = val.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        cs = w.curselection()
        print(value)
        self.entry1.delete(0, "end")
        self.entry1.insert(0, value)
        # set the value into the StringVar()
        self.Title.set(value)


def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print('You selected item %d: "%s"' % (index, value))
    cs = w.curselection()
    print(value)

    return value


def main():
    root = Tk()
    root.geometry("650x750")
    root.resizable(0, 0)
    app = UI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
