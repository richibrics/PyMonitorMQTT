import psutil
from Entities.Entity import Entity
import os



# Tip: customize topic because with more than one file, you must have different topics
TOPIC = 'file/file'

FILE_READ_SENSOR_FILENAME_CONTENTS_OPTION = "filename"

class FileReadSensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC)
        self.filename = self.GetOption([self.consts.CONTENTS_OPTION_KEY,FILE_READ_SENSOR_FILENAME_CONTENTS_OPTION])

    # I have also contents with filename (required) in config
    def EntitySchema(self):
        schema = super().EntitySchema()
        schema = schema.extend({
            self.schemas.Required(self.consts.CONTENTS_OPTION_KEY):  {
                self.schemas.Required(FILE_READ_SENSOR_FILENAME_CONTENTS_OPTION): str
            }
        })
        return schema

    def Update(self):
        if not self.FileExists():
            raise Exception("File must exist (and can't be a directory) !")
        with open(self.filename,"r") as f:
            self.SetTopicValue(TOPIC,f.read())

    def FileExists(self):
        return os.path.exists(self.filename) and os.path.isfile(self.filename)