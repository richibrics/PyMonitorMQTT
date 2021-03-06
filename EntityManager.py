import sys
import inspect
import time
from Logger import Logger, ExceptionTracker
from ClassManager import ClassManager

# Delay in second
update_rate = 20  # If not set in config


class EntityManager():
    # entities is a list of dicts: [{entity, mqtt_client, logger}]
    entities = []
    continue_sending = True  # Stop loop condition

    def __init__(self, config):
        self.config = config
        self.logger = Logger(config)
        self.classManager = ClassManager(config) # The one that loads and returns entities from Entities folder giving him only the name

    # ENTITIES MANAGEMENT PART

    def Start(self):
        # Start the send loop
        self.SendAllData()


    def ActiveEntities(self):
        return self.entities


    ## ENTITY POSTINITIALIZATION 

    def PostInitializeEntities(self):
        self.Log(Logger.LOG_DEBUG,"Starting post-initialization")
        for entity in self.entities:
            if not entity.postinitializeState:
                entity.CallPostInitialize()
        self.Log(Logger.LOG_DEBUG,"Finished post-initialization")


    ## ENTITY LOAD AND INITIALIZATION 

    # Here I receive the name of the entity (or maybe also the options) and pass it to a function to get the object
    # which will be initialized and appended in the list of entities
    # Here configs are specific for the monitor, it's not the same as this manager
    def LoadEntity(self, entity_suffix, entityString, monitor_id, config, mqtt_client, send_interval, logger):
        name = entityString
        options = None

        # If in the list I have a dict then I have some options for that command
        if type(entityString) == dict:
            name = list(entityString.keys())[0]
            options = entityString[name]

        obj = self.classManager.GetEntityClass(name+entity_suffix)
        if obj:
            try:
                objAlive = obj(monitor_id, config, mqtt_client,
                               send_interval, options, logger, self)
                if objAlive: # If initialize went great
                    self.entities.append(objAlive)
                    req = objAlive.LoadSettings()
                    # self.Log(Logger.LOG_INFO, name +
                    #         ' entity loaded', logger=logger)
                    return req  # Return the settings with equirements
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, ExceptionTracker.TrackString(
                    exc), logger=logger)
                self.Log(Logger.LOG_ERROR, name + " not loaded", logger=logger)
        return None

    def UnloadEntity(self, entity): # by entity object
        self.Log(Logger.LOG_WARNING, entity.name +
                 ' entity unloaded', logger=entity.GetLogger())
        self.entities.remove(entity)
        del(entity)

    def UnloadEntityByName(self, name, monitor_id): # by name and monitor id
        self.UnloadEntity(self.FindEntities(name, monitor_id)[0])  # HEREEE

    def FindEntities(self, name, monitor_id):
        # Return the entity object present in entities list: to get entity value from another entity for example
        entities = []
        for entity in self.ActiveEntities():
            # If it's an object->obj.name, if a class must use the .__dict__ for the name
            if name == entity.name and monitor_id == entity.GetMonitorID():
                entities.append(entity)
        return entities



    ## ENTITIES OUTGOING DATA (AKA SENSOR ENTITIES) PART

    def SendSensorsData(self):
        for sensor in self.entities:
            sensor.SendData()

    # Also discovery data every X second
    def SendAllData(self):
        while self.continue_sending:
            for entity in self.ActiveEntities():
                if entity.GetMqttClient().connected:
                    if entity.ShouldSendMessage():  # HERE CHECK IF HAS OUTTOPICS
                        entity.CallUpdate()
                        entity.SendData()
                        # Save this time as time when last message is sent
                        entity.SaveTimeMessageSent()
                        self.Log(Logger.LOG_DEBUG,"Sending " + entity.name)
                    if entity.ShouldSendDiscoveryConfig():
                        try:
                            discovery_data = entity.PrepareDiscoveryPayloads()
                            discovery_data = entity.ManageDiscoveryData(
                                discovery_data)
                            entity.PublishDiscoveryData(discovery_data)
                            entity.SaveTimeDiscoverySent()
                        except Exception as e :
                            self.Log(Logger.LOG_ERROR, "Error while preparing discovery configuration for " + entity.name + ": " + str(e))
                            self.UnloadEntity(entity)
            time.sleep(1)  # Wait a second and recheck if someone has to send


    # LOG

    def Log(self, messageType, message, logger=None):
        if logger is None:
            logger = self.logger
        logger.Log(messageType, 'Entity Manager', message)
