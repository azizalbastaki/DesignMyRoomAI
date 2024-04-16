# import panda3d
from direct.showbase.ShowBase import ShowBase
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
                            initialText="Describe the room", numLines=30, width = 15,cursorKeys = 1, focus=1
                                    , parent=base.a2dTopLeft, pos=(0.01, 0, -0.3))
        render.setShaderAuto()
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
            newModel.setPos(float(finalPropertyList[1]), float(finalPropertyList[2]), float(finalPropertyList[3]))
            newModel.setHpr(float(finalPropertyList[4]), float(finalPropertyList[5]), float(finalPropertyList[6]))
            newModel.setColor(float(finalPropertyList[7]), float(finalPropertyList[8]), float(finalPropertyList[9]), float(finalPropertyList[10]))
            newModel.setScale(float(finalPropertyList[11]))


        print(objectList)
        return

    def promptEngineered(self, textEntered):
        modelsAvailable = str(os.listdir("assets/furniture"))

        prompt = "You will receive a description of a room. The response you provide will be used to load several 3D models into a 3D cartesian space. You must provide a list of models that would be loaded, alongside several properties such as color, size, position (z up, also bounds are 20 units), and rotation (heading, pitch, roll). The files available are: " + modelsAvailable + ". Use these exact filenames ONLY and MAKE SURE THEY EXIST, there is no sofa.glb SO DO NOT USE IT BECAUSE IT DOESN'T EXIST. Please provide a in the following format: [{filename} {posX} {posY} {posZ} {heading} {pitch}, {roll} {color_red - 0 to 1} {color_blue - 0 to 1} {color_green - 0 to 1} {color_alpha - 0 to 1} {scale}], each object in its own line. INCLUDE THE FILE EXTENSION IN FILENAME TOO. So for example, ({books.glb}{0}{0}{0}{90}{20}{0}{1}{0}{0.5}{0.4}{1}). Please ensure that walls and floorings are also specified,  The input is as follows: "
        response = self.model.generate_content(prompt + textEntered)
        #print(response.text)

        return response.text



app = MyApp()
app.run()