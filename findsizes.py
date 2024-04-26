import os
models = (os.listdir("assets/furniture"))
print(models)
from panda3d.core import loadPrcFileData
loadPrcFileData("", "window-type offscreen")
from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.models = models
        self.sizes = {}
        for model in self.models:
            if not model.endswith(".glb"):
                continue
            self.model = loader.loadModel(f"assets/furniture/{model}")
            bounds = self.model.getTightBounds()
            size = bounds[1] - bounds[0]
            scalesize = int(size.length() + 1)
            self.sizes[model] = scalesize
        with open("sizes.txt", 'w') as file:
            file.write(str(self.sizes))
        file.close()
        self.destroy()

app = MyApp()
