
import os, playsound, sys
import random
import asyncio
from pydub import AudioSegment
from pydub.playback import play



class PoopVoiceLines:
    
    
    def __init__(self, dirname="voiceLines"):
        self.voiceLines = {
            "Jayne" : ["sploosh1.mp3", 
                    "PerfectlyAimed.mp3",
                    "prizePoop1.mp3",
                    "PerfectlyAimed2.mp3", 
                    "prizePoop2.mp3",
                    "sploosh2.mp3",
                    "prizePoop3.mp3",
                    "tryAnother.mp3",
                    "thatTheShit.mp3",
                    "paidForThat.mp3",
                    "tryAnother2.mp3",
                    "thatTheShit2.mp3",
                    "doThatMore.mp3",
                    "turd_hit_bowl1.mp3",
                    "turd_hit_bowl2.mp3"],
            "Ren" : ["NiceDunk3.mp3",
                    "NicePoop3.mp3",
                    "NiceDunk.mp3",
                    "NiceDunk2.mp3",
                    "NiceDump.mp3",
                    "NicePoop2.mp3",
                    "NiceDump2.mp3",
                    "NicePoop.mp3",
                    "goodSploosh2.mp3",
                    "goodSploosh.mp3",
                    "GoodAtThis2.mp3",
                    "CongratsOnShit.mp3",
                    "PrizeWinning.mp3",
                    "PrizeWinning2.mp3",
                    "GoodAtThis.mp3",
                    "SoundedGreat.mp3",
                    "LessToWorry2.mp3",
                    "thatTheShit.mp3",
                    "thatTheShit2.mp3",
                    "SoundedGreat2.mp3",
                    "jobWellDone2.mp3",
                    "MoreOften.mp3",
                    "paidForThat.mp3",
                    "TalkingAbout.mp3",
                    "jobWellDone.mp3",
                    "TryAnother2.mp3",
                    "LessToWorry.mp3",
                    "MoreOften2.mp3",
                    "SoRelieved2.mp3",
                    "TryAnother.mp3",
                    "turdHitBowl.mp3",
                    "SoRelieved.mp3",
                    "HearCorrectly2.mp3",
                    "HearCorrectly1.mp3",
                    "SplashButthole.mp3"],
            "rgarnevo" : ["NicePooP.mp3",
                    "niceDump2.mp3",
                    "niceDump.mp3",
                    "PrizeWinning.mp3",
                    "PerfectlyAimed.mp3",
                    "sploosh.mp3",
                    "ExcellentlyShat.mp3",
                    "goodAtThis.mp3",
                    "oneLessThing.mp3",
                    "DoThatMoreOften.mp3",
                    "ThatSoundedGreat.mp3",
                    "paidForThat.mp3",
                    "JobWellDone.mp3",
                    "whatImTalkin.mp3",
                    "hearCorrectly.mp3",
                    "tryAnother.mp3",
                    "turdHitTheBowl.mp3",
                    "SoLoudItSplash.mp3",
                    "relief.mp3",
                    "thatsTheSHIT.mp3"],
        }
        self.constipationLines = {
            "Jayne" : ["evacuateBowels.mp3",
                    "evacuateBowels2.mp3",
                    "pushYoucan.mp3",
                    "pushYoucan2.mp3"],
            "Ren" : ["BowelEvacuation.mp3",
                    "keepGoing.mp3",
                    "keepGoing2.mp3",
                    "NotAlwaysSuccess.mp3",
                    "squeeze.mp3"],
            "rgarnevo" : ["DontStop.mp3",
                    "squeeze.mp3",
                    "thingsDontComeout.mp3"]
        }
        self.notFoundLines = {
            "Jayne" : [],
            "Ren" : [],
            "rgarnevo" : []
        }
        self.notFoundLinesConstipation = {
            "Jayne" : [],
            "Ren" : [],
            "rgarnevo" : []
        }
        self.dirname = dirname
        self.isPlaying = False
        random.seed()
        self.checkFileIntegrity()

    def getPathToLine(self, voiceActor : str, index, lineType="splash"):
        if (lineType == "constipation"):
            ret = f"{self.dirname}/{lineType}/{voiceActor}/{self.constipationLines[voiceActor][index]}"
        else:
            ret = f"{self.dirname}/{lineType}/{voiceActor}/{self.voiceLines[voiceActor][index]}"
        return ret

    def checkFileIntegrity(self):
        """
        This will check if all the files defined on the members are available. If one is not, an error will be displayed
        and the file will be blacklisted from being used.
        """
        for actor in ["Jayne", "Ren", "rgarnevo"]:
            for i in range(len(self.voiceLines[actor])):
                if (not os.path.exists(self.getPathToLine(actor, i))):
                    print(f"Failed to find {self.getPathToLine(actor, i)}", file=sys.stderr)
                    self.notFoundLines[actor].append(i)
            l_set = set(self.voiceLines[actor])
            if (len(l_set) != len(self.voiceLines[actor])):
                print(f"There are duplicates on the voiceLines of {actor}", file=sys.stderr)
        for actor in ["Jayne", "Ren", "rgarnevo"]:
            for i in range(len(self.constipationLines[actor])):
                linePath = self.getPathToLine(actor, i, lineType="constipation")
                if (not os.path.exists(linePath)):
                    print(f"Failed to find {linePath}", file=sys.stderr)
                    self.notFoundLinesConstipation[actor].append(i)
            l_set = set(self.constipationLines[actor])
            if (len(l_set) != len(self.constipationLines[actor])):
                print(f"There are duplicates on the constipationLines of {actor}", file=sys.stderr)
    
    async def __playLineAsync(self, path):
        self.isPlaying = True
        playsound.playsound(path)
        self.isPlaying = False

    def playLineWait(self, path):
        sound = AudioSegment.from_mp3(path)
        play(sound)
    
    def playSpecificLine(self, voiceActor, lineName):
        for i in range(len(self.voiceLines[voiceActor])):
            if lineName == self.voiceLines[voiceActor][i] or lineName == self.voiceLines[voiceActor][i][0:-4]:
                #asyncio.run(self.__playLineAsync(self.getPathToLine(voiceActor, i)))
                self.playLineWait(self.getPathToLine(voiceActor, i))
                return
        for i in range(len(self.constipationLines[voiceActor])):
            if lineName == self.constipationLines[voiceActor][i] or lineName == self.constipationLines[voiceActor][i][0:-4]:
                #asyncio.run(self.__playLineAsync(self.getPathToLine(voiceActor, i, lineType="constipation")))
                self.playLineWait(self.getPathToLine(voiceActor, i, lineType="constipation"))
                return
        print(f"Failed to find {voiceActor}'s {lineName}", file=sys.stderr)

    
    def playRandomLineFrom(self, voiceActor, lineType="splash"):
        possible = []
        if (lineType == "splash"):
            for i in range(len(self.voiceLines[voiceActor])):
                if (not (i in self.notFoundLines[voiceActor])):
                    possible.append(i)
        elif (lineType == "constipation"):
            for i in range(len(self.constipationLines[voiceActor])):
                if (not (i in self.notFoundLinesConstipation[voiceActor])):
                    possible.append(i)
        else:
            print(f"There is no voice line type {lineType}", file=sys.stderr)
            return
        if (possible == []):
            print(f"No voicelines available for {voiceActor}", file=sys.stderr)
            return
        i = random.choice(possible)
        #asyncio.run(self.__playLineAsync(self.getPathToLine(voiceActor, i, lineType=lineType)))
        self.playLineWait(self.getPathToLine(voiceActor, i, lineType=lineType))

    def playRandomLine(self, lineType="splash"):
        actor = random.choice(["Jayne", "Ren", "rgarnevo"])
        self.playRandomLineFrom(actor, lineType=lineType)
