import time, datetime
import os
import spotipy
import webbrowser
import spotipy.util as util
import random
from subprocess import call



class Spotify:

    def __init__(self):
        self.username = input("Enter username > ")
        self.userScope = 'user-library-read user-read-private'
        self.spotipyObject = self.createSpotipyObject()
        self.userData = self.getUserData()

    def createSpotipyObject(self):
        return spotipy.Spotify(auth=self.getUserToken())

    def getUserToken(self):
        try:
            token = util.prompt_for_user_token(self.username, scope=self.userScope, client_id='041eb8754fb14e76970bd74d88537edf', client_secret='x', redirect_uri='https://google.com/')
        except Exception as e:
            os.remove(f".cache-{self.username}")
            self.getUserToken()

        return token

    def getUserData(self):
        return self.spotipyObject.current_user()

    def getSubscriptionType(self):
        return self.userData['product']

    def playRandomSong(self):
        if (self.getSubscriptionType() == "premium"):
            self.spotipyObject.start_playback(uris=[self.pickRandomSong()])
        else:
            webbrowser.open(self.pickRandomSong())
        # time.sleep(30)
        # self.playRandomSong()  continue until user stops program, or max recursion reached -- currently disabled

    def createSongList(self):
        tracks = self.spotipyObject.current_user_saved_tracks(limit=50)
        songList = []
        if (self.getSubscriptionType() == "premium"):
            for track in tracks['items']:
                songList.append(track["track"]["uri"])
        else:
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




class AudioController: # works on linux 

    def __init__(self):
        self.currentVolume = 45
    
    def incrementAudioLevel(self):
        call(["amixer", "-D", "pulse", "sset", "Master", f"{self.currentVolume}%"])
        self.currentVolume += 5
    

def main():
    spotify = Spotify()
    clock = Clock(Clock.getTimeForWakingUp())
    audio = AudioController()
    audio.incrementAudioLevel() # set audio to 45% -- only linux
    
    while not clock.checkHour(): 
        time.sleep(60)  # wait for one minute before checking again, in order to reduce resource usage
    
    spotify.playRandomSong()

    while audio.currentVolume < 100:
        time.sleep(1)
        # audio.incrementAudioLevel() -- only linux






if __name__ == '__main__':
    main()
