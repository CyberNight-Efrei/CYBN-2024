import json
from core.utils import Encoding, Mode

class Config:
    def __init__(self, config_file, defaults):
        self.config = defaults
        with open(config_file, 'r') as file:
            self.config.update(json.load(file))
        self.config["encoding_type"] = Encoding(self.config["encoding_type"])
        self.config["encoding_mode"] = Mode(self.config["encoding_mode"])

    def __getattr__(self, item):
        if item in self.config:
            return self.config[item]
        else:
            raise AttributeError(f"'Config' object has no attribute '{item}'")

# Default values
defaults = {
    "codec": "MJPG",
    "fps": 25,
    "extension": ".avi",
    "filename": "video",
    "tmp_archive": "tmp/archive.zip",
    "encoding_type": 2,
    "encoding_mode": 0,
}

# Load config file with default values
config = Config('config.json', defaults)