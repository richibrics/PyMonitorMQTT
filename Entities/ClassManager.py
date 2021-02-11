import os
from Entities.Entity import Entity
from pathlib import Path
from os import path
import importlib.util
import importlib.machinery
import sys, inspect
from Logger import Logger


class ClassManager(): # Class to load Entities from the Entitties dir and get them from name 
    def __init__(self,logger):
        self.logger=logger
        self.modulesFilename=[]
        self.classPath = path.dirname(path.abspath(
            sys.modules[self.__class__.__module__].__file__))
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
        self.Log(Logger.LOG_DEVELOPMENT,"Now I get entities files...")
        result = list(Path(path.join(self.classPath,".")).rglob("*.py"))
        entities = []
        for file in result:
            filename = str(file)
            if len(filename.split(os.sep)) >= 3: # only files in subfolders
                entities.append(filename)
                self.Log(Logger.LOG_DEVELOPMENT,filename)
        self.modulesFilename = entities

    def ModuleNameFromPath(self,path):
        classname=os.path.split(path)
        return classname[1][:-3] 

    def Log(self,type,message):
        self.logger.Log(type,"Class Manager",message)