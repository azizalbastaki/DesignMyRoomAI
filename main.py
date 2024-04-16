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
                            initialText="TV facing a sofa", numLines=30, width = 15,cursorKeys = 1, focus=1
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
        for object in self.assetsLoaded:
            object.removeNode()
        again = True
        while again:
            again = False
            try:
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
                    if len(finalPropertyList) == 4:
                        newModel.setPos(float(finalPropertyList[1]), float(finalPropertyList[2]), 0)
                        newModel.setHpr(float(finalPropertyList[3]), 90, 0)
                        newModel.setScale(1)
                    else:
                        newModel.setX(float(finalPropertyList[1]), self.assetsLoaded[-2])
                        newModel.setHpr(float(finalPropertyList[2]), 90, 0)
                    newModel.setScale(1)

                print(objectList)
            except:
                print("Tried to load missing model")
                again = True
        return

    def promptEngineered(self, textEntered):
        modelsAvailable = open("sizes.txt", 'r').read()
        print(modelsAvailable)
        prompt = '''
This is an app that will take an input from the user and, using the models available, generate a room. The response you provide will be used to load several models into a 3D space, use only the files listed, nothing else, do not make up files. Use only the files available, and those are as follows (also keep note of the sizes when setting out the room, they're provided as a Vec3 format): ''' + modelsAvailable + '''. Use these exact filenames ONLY and MAKE SURE THEY EXIST, there is no sofa.glb nor is there a tablelamp SO DO NOT USE IT BECAUSE IT DOESN'T EXIST. Please provide in the following format:
{filename} {posX} {posY} {heading}] OR {filename} {relativePos} {heading}, each object in its own line. INCLUDE THE FILE .glb EXTENSION IN FILENAME TOO. So for example, {books.glb}{0}{0}{90}. 

{filename} - the name of the file, for example “{char.glb}”
{posX} - a value between -5 and 5. 
{posY} - a value between -5 and 5.
{heading} - a value between 0 and 360 - the direction the object is facing. Keep in mind that all objects are facing the negative y axis when H (heading) is equal to 0.
{relativePos} - linear distance relative to previous object between -5 and 5, so or example {3} would mean 3 spaces in front of the last object added.
All values between curly brackets
FOR DOORWAYS, POS X MUST EITHER BE -5 OR 5 OR POS Y MUST BE -5 OR 5
AND DO NOT PROVIDE VALUES OUTSIDE GIVEN RANGES. DO NOT INSTANTIATE MORE THAN 30 OBJECTS. The input is as follows:
'''
        response = self.model.generate_content(prompt + textEntered)
        #print(response.text)

        return response.text



app = MyApp()
app.run()