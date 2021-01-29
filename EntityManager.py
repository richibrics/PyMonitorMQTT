import sys
import inspect
import time
from Logger import Logger

import signal # To catch interrupt signals

# Delay in second
update_rate = 20  # If not set in config


class EntityManager():
    # entities is a list of dicts: [{entity, mqtt_client, logger}]
    entities = []
    continue_sending = True  # Stop loop condition

    def __init__(self, config):
        self.config = config
        self.logger = Logger(config)

    def Start(self):
        # Start the send loop
        self.SendAllData()

    def PostInitializeSensors(self):
        for entity in self.entities:
            try:
                entity.PostInitialize()
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, entity.name +
                         ': error during post-initialization')
                self.Log(Logger.LOG_ERROR,
                         Logger.ExceptionTracker.TrackString(exc))
                self.UnloadEntity(entity.name, entity.GetMonitorID())

    # Here I receive the name of the entity (or maybe also the options) and pass it to a function to get the object
    # which will be initialized and appended in the list of entities
    # Here configs are specific for the monitor, it's not the same as this manager

    def LoadEntity(self,entity_suffix, module_name,entityString, monitor_id, config, mqtt_client, send_interval, logger):
        name = entityString
        options = None

        # If in the list I have a dict then I have some options for that command
        if type(entityString) == dict:
            name = list(entityString.keys())[0]
            options = entityString[name]

        obj = self.GetEntityObjectByName(entity_suffix, module_name,name)
        if obj:
            try:
                objAlive = obj(monitor_id, config, mqtt_client,
                               send_interval, options, logger, self)
                self.entities.append(objAlive)
                req = objAlive.LoadSettings()
                self.Log(Logger.LOG_INFO, name +
                         ' entity loaded', logger=logger)
                return req  # Return the settings with equirements
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, name +
                         ' entity occured an error during loading: ' + str(exc), logger=logger)
                self.Log(Logger.LOG_ERROR, Logger.ExceptionTracker.TrackString(
                    exc), logger=logger)
        return None

    def UnloadEntity(self, name, monitor_id):
        obj = self.FindEntity(name, monitor_id) # HEREEE
        self.Log(Logger.LOG_WARNING, name +
                 ' entity unloaded', logger=obj.GetLogger())
        self.entities.remove(obj)

    def FindEntities(self, name, monitor_id):
        # Return the entity object present in entities list: to get entity value from another entity for example
        entities = []
        for entity in self.ActiveEntities():
            # If it's an object->obj.name, if a class must use the .__dict__ for the name
            if name == entity.name and monitor_id == entity.GetMonitorID():
                entities.append(entity)
        return entities

    def ActiveEntities(self):
        return self.entities

    def GetEntityObjectByName(self, entity_suffix, module_name, name):
        entitiesList = self.GetObjectsList(entity_suffix, module_name)
        for entity in entitiesList:
            if name == self.GetEntityName(entity,entity_suffix):
                return entity
        self.Log(Logger.LOG_ERROR, str(name) + ' ' + entity_suffix  + ' not found - check the module import line is added'
                                               ' to ' + module_name +  '/__init__.py')
        return None

    def GetObjectsList(self,entity_suffix, module_name):
        classes = []
        for name, obj in inspect.getmembers(sys.modules[module_name]):
            if inspect.isclass(obj):
                # Don't add the .parent class to the list
                if(("."+entity_suffix) not in self.GetClassName(obj)):
                    classes.append(obj)
        return classes

    def UpdateSensors(self):
        for sensor in self.entities:
            sensor.CallUpdate()

    def SendSensorsData(self):
        for sensor in self.entities:
            sensor.SendData()

    def GetClassName(self, entity_class):
        # Sensor.SENSORFOLDER.SENSORCLASS
        return entity_class.__dict__['__module__']

    def GetEntityName(self, entity_class, name_suffix):
        # Only SENSORCLASS (without Sensor suffix)
        return self.GetClassName(entity_class).split('.')[-1].split(name_suffix)[0]

    # Also discovery data every X second
    def SendAllData(self):
        while self.continue_sending:
            for entity in self.ActiveEntities():
                if entity.GetMqttClient().connected:
                    if entity.ShouldSendMessage(): # HERE CHECK IF HAS OUTTOPICS
                        entity.CallUpdate()
                        entity.SendData()
                        # Save this time as time when last message is sent
                        entity.SaveTimeMessageSent()            
                    if entity.ShouldSendDiscoveryConfig():
                        discovery_data = entity.PrepareDiscoveryPayloads()
                        discovery_data = entity.ManageDiscoveryData(discovery_data)
                        entity.PublishDiscoveryData(discovery_data)
                        entity.SaveTimeDiscoverySent()
            time.sleep(1)  # Wait a second and recheck if someone has to send
            


    def Log(self, messageType, message, logger=None):
        if logger is None:
            logger = self.logger
        logger.Log(messageType, 'Entity Manager', message)

