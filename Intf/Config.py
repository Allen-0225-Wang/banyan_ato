
from configparser import ConfigParser

class Config(object):
    hosts=""

    @classmethod
    def getCfg(cls):
        conf = ConfigParser()
        conf.read("server.ini")
        host = conf.get("server", "host")
        port = conf.get("server", "port")
        cls.hosts = host + ':' + port

    @classmethod
    def getHosts(cls):
        return cls.hosts
