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
                            initialText="TV and sofa facing each other", numLines=30, width = 15,cursorKeys = 1, focus=1
                                    , parent=base.a2dTopLeft, pos=(0.01, 0, -0.3), text_fg = (1,1,1,1))
        self.entrybox.setColor(0.1,0.1,0.1,0.7)
        dlight = DirectionalLight('dlight')
        dlight.setColor((0.8, 0.8, 0.5, 1))
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)
        # add floor and 4 walls
        floor = loader.loadModel("assets/environment/floorFull.glb")
        floor.reparentTo(render)
        floor.setPos(-5, -5, 0)
        floor.setScale(10)
        floor.setSy(0.01)
        floor.setHpr(0, 90, 0)
        # wall1 = loader.loadModel("assets/environment/wall.glb")
        # wall1.reparentTo(render)
        # wall1.setPos(5, 5, 0)
        # wall1.setScale(10)
        # wall1.setHpr(0, 90, 0)
        # wall2 = loader.loadModel("assets/environment/wall.glb")
        # wall2.reparentTo(render)
        # wall2.setPos(5, -5, 0)
        # wall2.setScale(10)
        # wall2.setHpr(0, 90, 0)
        # wall3 = loader.loadModel("assets/environment/wall.glb")
        # wall3.reparentTo(render)
        # wall3.setPos(-5, 5, 0)
        # wall3.setScale(10)
        # #wall3.setHpr(0, 90, 0)
        # wall4 = loader.loadModel("assets/environment/wall.glb")
        # wall4.reparentTo(render)
        # wall4.setPos(5, 5, 0)
        # wall4.setScale(10)
        # #wall4.setHpr(0, 90, 0)

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
                    newModel.setPos(float(finalPropertyList[1]), float(finalPropertyList[2]), 0)
                    newModel.setHpr(float(finalPropertyList[3])-180, 90, 0)
                    #newModel.setScale(1)

                print(objectList)
            except Exception as error:
                print(error)
                again = True
        return

    def promptEngineered(self, textEntered):
        modelsAvailable = open("sizes.txt", 'r').read()

        firstStage = self.model.generate_content("Imagine you're playing with legos and have a 10x10 grid to work with, and you have the following bricks - each brick is a square and its side length is noted along with the name: " + modelsAvailable + " - list out all the coordinates and direction of where you'd place the furniture (no need to use all of them, just ones you'd need for the description that will follow this) as well as the direction in heading (up to 360, an object pointing at 0 points at the negative y axis)" + ''', 
        so for example, if the prompt was TV and sofa facing each other, the answer should be: 
        - televisionModern.glb: (0, 1), 180 degrees
        - loungeSofa.glb: (0, -1), 0 degrees
        no overlapping is allowed (SO NO TWO OBJECTS SHARE THE SAME COORDINATE), bottom left coordinate is (-5,-5), PLEASE CONSIDER THE NECESSITY OF USING EACH BRICK, FOR EXAMPLE THERE IS NO BED IN A STANDARD CLASSROOM OR LIVING ROOM, the prompt is as follows: ''' + textEntered)
        print("First stage text")
        print(firstStage.text)
        print(modelsAvailable)
        prompt = '''
Using only the following files: ''' + modelsAvailable + '''. Use these exact filenames ONLY and MAKE SURE THEY EXIST, there is no sofa.glb nor is there a tablelamp.glb SO DO NOT USE IT BECAUSE IT DOESN'T EXIST. Please turn the following input in to the following format:
{filename} {posX} {posY} {heading}], each object in its own line. INCLUDE THE FILE .glb EXTENSION IN FILENAME TOO. So for example, {books.glb} {0} {0} {90}. 

{filename} - the name of the file, for example “{char.glb}”
{posX} - a value between -5 and 5. 
{posY} - a value between -5 and 5.
All values must be between curly brackets
{heading} - a value between 0 and 360 - the direction the object is facing. Keep in mind that all objects are facing the negative y axis when H (heading) is equal to {0}, make sure the direction they're facing makes contextual sense.
AND DO NOT PROVIDE VALUES OUTSIDE GIVEN RANGES. DO NOT LIST MORE THAN 10 OBJECTS, NO TWO MODELS MAY SHARE THE SAME COORDINATE, YOU MAY ONLY USE THE FOLLOWING FILES: ''' + modelsAvailable + "The input is as follows: "

        response = self.model.generate_content(prompt + firstStage.text)
        #print(response.text)

        return response.text



app = MyApp()
app.run()