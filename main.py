# import panda3d
from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight
from direct.gui.DirectGui import *
import google.generativeai as genai
import os

def getAPIKey():
    file = open("api_key.txt", 'r')
    key = file.read()
    file.close()
    return key
genai.configure(api_key=getAPIKey())


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.model = genai.GenerativeModel('gemini-pro')
        self.keyMap = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "p": False,
            "l": False
        }


        self.assetsLoaded = []

        self.accept("a", self.updateKey, ["left", True])
        self.accept("a-up", self.updateKey, ["left", False])

        self.accept("s", self.updateKey, ["down", True])
        self.accept("s-up", self.updateKey, ["down", False])

        self.accept("d", self.updateKey, ["right", True])
        self.accept("d-up", self.updateKey, ["right", False])

        self.accept("w", self.updateKey, ["up", True])
        self.accept("w-up", self.updateKey, ["up", False])

        self.accept("p", self.updateKey, ["p", True])
        self.accept("p-up", self.updateKey, ["p", False])

        self.accept("l", self.updateKey, ["l", True])
        self.accept("l-up", self.updateKey, ["l", False])

        self.entrybox = DirectEntry(text="", scale=0.05, command=self.designRoom,
                            initialText="Describe a standard living room", numLines=30, width = 15,cursorKeys = 1, focus=1
                                    , parent=base.a2dTopLeft, pos=(0.01, 0, -0.3), text_fg = (1,1,1,1))
        self.entrybox.setColor(0.1,0.1,0.1,0.7)
        self.entrybox.set
        dlight = DirectionalLight('dlight')
        dlight.setColor((0.8, 0.8, 0.5, 1))
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)
        self.taskMgr.add(self.update, "update")
    def updateKey(self, key, value):
        self.keyMap[key] = value
    def update(self, task):
        return task.cont

    def designRoom(self, textEntered):
        print(textEntered)
        self.assetsLoaded = []
        response = self.promptEngineered(textEntered)
        objectList = response.split("\n")
        print(objectList)
        for obj in range(0, len(objectList)):
            objectList[obj] = objectList[obj].replace("{", "").split("}")
            objectList[obj].pop()
            finalPropertyList = objectList[obj]
            newModel = loader.loadModel("assets/furniture/" + objectList[obj][0])
            self.assetsLoaded.append(newModel)
            newModel.reparentTo(render)
            newModel.setPos(float(finalPropertyList[1]), float(finalPropertyList[2]), 0)
            newModel.setHpr(float(finalPropertyList[3]), 90, 0)
            newModel.setScale(1)

        print(objectList)
        return

    def promptEngineered(self, textEntered):
        modelsAvailable = str(os.listdir("assets/furniture"))
        print(modelsAvailable)
        prompt = "you will receive a description of a room. Using only the models available, you must provide a list of models that would be loaded, alongside several properties such position, and heading. The files available are. USE THOSE ONLY, DO NOT MAKE UP ANY FILE: " + modelsAvailable + ". Use these exact filenames ONLY and MAKE SURE THEY EXIST, there is no sofa.glb nor is there a tablelamp SO DO NOT USE IT BECAUSE IT DOESN'T EXIST. Please provide a in the following format: [{filename} {posX values between -5 to 5} {posY - values between -5 to 5}{posY - values between 0 to 10} {heading}], each object in its own line. INCLUDE THE FILE EXTENSION IN FILENAME TOO. So for example, ({books.glb}{0}{0}{90}). AND DO NOT PROVIDE VALUES OUTSIDE GIVEN RANGES, doorways must either have a x value of 0 or y value of 0,  The input is as follows: "
        response = self.model.generate_content(prompt + textEntered)
        #print(response.text)

        return response.text



app = MyApp()
app.run()