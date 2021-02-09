import os
from Entities.Entity import Entity
from pathlib import Path
import importlib.util
import importlib.machinery
import sys, inspect

class ClassManager(): # Class to load Entities from the Entitties dir and get them from name 
    def __init__(self):
        self.modulesFilename=[]
        self.GetModulesFilename() 

    def GetEntityClass(self,entityName):
        # From entity name, load the correct module and extract the entity class
        for module in self.modulesFilename: # Search the module file
            moduleName=self.ModuleNameFromPath(module)
            # Check if the module name matches the entity sname
            if entityName==moduleName:
                # Load the module
                loadedModule=self.LoadModule(module)
                return self.GetEntityClassFromModule(loadedModule)
        return None


    def LoadModule(self,path): # Get module and load it from the path
        loader = importlib.machinery.SourceFileLoader(self.ModuleNameFromPath(path), path)
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        moduleName=os.path.split(path)[1][:-3]
        sys.modules[moduleName]=module
        return module

    def GetEntityClassFromModule(self,module): # From the module passed, I search for a Class that has the Entity class as parent
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                for base in obj.__bases__: # Check parent class
                    if(base==Entity):
                        return obj


    def GetModulesFilename(self): # List files in the Entities directory and get only files in subfolders
        result = list(Path("Entities/.").rglob("*.py"))
        entities = []
        for file in result:
            filename = str(file)
            if len(filename.split(os.sep)) >= 3: # only files in subfolders
                entities.append(filename)
        self.modulesFilename = entities

    def ModuleNameFromPath(self,path):
        classname=os.path.split(path)
        return classname[1][:-3] 