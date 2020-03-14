import time, datetime
import os, sys
import spotipy
import webbrowser
import spotipy.util as util
import json
import json.decoder as JSONDecodeError
import random




class Spotify:

    def __init__(self):
        self.username = input("Enter username > ")
        self.userScope = 'user-library-read'
        self.spotipyObject = self.createSpotipyObject()
        self.userData = self.getUserData()

    def createSpotipyObject(self):
        return spotipy.Spotify(auth=self.getUserToken())

    def getUserToken(self):
        try:
            token = util.prompt_for_user_token(self.username, scope=self.userScope, client_id='041eb8754fb14e76970bd74d88537edf', client_secret='6465e55750664185a0ba6fdecb8147b7', redirect_uri='https://google.com/')
        except Exception as e:
            os.remove(f".cache-{self.username}")
            self.getUserToken()

        return token

    def getUserData(self):
        return self.spotipyObject.current_user()


    def playRandomSong(self):
        webbrowser.open(self.pickRandomSong())
        # time.sleep(30)
        # self.playRandomSong()  continue until user stops program, or max recursion reached, currently disabled

    def createSongList(self):
        tracks = self.spotipyObject.current_user_saved_tracks(limit=50)
        songList = []
        for track in tracks['items']:
            songList.append(track["track"]["preview_url"])
        return songList

    def pickRandomSong(self):
        songs = self.filterSongList(self.createSongList())
        picked_song = random.choice(songs)
        return picked_song
    
    @staticmethod
    def filterSongList(songs):
        ret = []
        for song in songs:
            if song != None:
                ret.append(song)
        return ret
    
    

    

        



class Clock:

    def __init__(self, wakeuptime):
        self.time = wakeuptime
    
    @staticmethod
    def getTimeForWakingUp():
        return [int(input("hour > ")), int(input("minute > "))]
    
    def checkHour(self):
        currentTime = datetime.datetime.now()
        return self.time[0] == currentTime.hour and self.time[1] == currentTime.minute



def main():
    spotify = Spotify()
    clock = Clock(Clock.getTimeForWakingUp())
    while not clock.checkHour(): 
        time.sleep(60)  # wait for one minute before checking again, in order to reduce resource usage
    spotify.playRandomSong() 




if __name__ == '__main__':
    main()