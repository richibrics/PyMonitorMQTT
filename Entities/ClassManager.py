import os
import Entities
from pathlib import Path
import importlib.util
import importlib.machinery

class ClassManager(): # Class to  load Entities in the Entitties dir and get them from name 
    def __init__(self):
        pass

    def LoadAllEntities(self):
        print(self.LoadAllModules())

    def LoadAllModules(self):
        loadedModules = []
        modules=self.RecursiveListEntitiesPy()

        for module in modules:
            classname=os.path.split(module)
            classname=classname[len(classname)-1][:-3]

            loader = importlib.machinery.SourceFileLoader(classname, module)
            spec = importlib.util.spec_from_loader(loader.name, loader)
            mod = importlib.util.module_from_spec(spec)
            loader.exec_module(mod)
            loadedModules.append(mod)
        
        return loadedModules
            
    def RecursiveListEntitiesPy(self):
        result = list(Path("Entities/.").rglob("*.py"))
        entities = []
        for file in result:
            filename = str(file)
            if "/" in filename:
                if len(filename.split("/")) >= 3:
                    entities.append(filename)
            elif "\\" in filename:
                if len(filename.split("\\")) >= 3:
                    entities.append(filename)
        return entities
