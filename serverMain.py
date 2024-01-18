from modules.sensorMon import sensorMonModule
from modules.hCOM import hComModule
from yaml import safe_load
import logging

logging.basicConfig(level = logging.NOTSET, format = "%(levelname)s %(asctime)s - %(message)s", handlers=[logging.FileHandler("serverLogFile.log", mode='w')])    

# creating monitorizing tools
sensorHandler = sensorMonModule()

# importing configurations
try:
    with open("config.yaml") as file: configurations = safe_load(file)
    logger = logging.getLogger(configurations["logging_idendity"])
    logger.info("Configurations successfully imported")
except Exception as e:
    logger.warning("Failed to import configurations")
    logger.critical(e)

# creating communication handler
try:
    comPipe = hComModule(configurations['communication'], 
                     serverIP = "localhost", 
                     comRole = "SW", 
                     logging_identity = configurations["logging_idendity"], 
                     sensorHandler = sensorHandler)
    comPipe.initPipe()
    comStat = True
    logger.info("Communication handler successfully initialized")
except Exception as e:
    comStat = False
    logger.warning(e)
    logger.critical("Failed to initialize communication handler")


while True:
    comPipe.serverSendMsg(input("MSG : "))