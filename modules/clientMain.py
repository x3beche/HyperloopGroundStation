from modules.hCOM import hComModule
from yaml import safe_load
from time import sleep, time
from json import loads
import logging

# variables
file_path = str(__file__).replace("ClientMain.py","")

# logging settings
logging.basicConfig(level = logging.NOTSET, format = "%(levelname)s %(asctime)s - %(message)s", handlers=[logging.FileHandler("clientLogFile.log", mode='w')])    

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
                         serverIP = "192.168.1.40", 
                         comRole = "CL", 
                         logging_identity = configurations["logging_idendity"])
    comPipe.initPipe()
    comStat = True
    logger.info("Communication handler successfully initialized")
except Exception as e:
    comStat = False
    logger.warning(e)
    logger.critical("Failed to initialize communication handler")


while True:
    comPipe.send("getSensorValues")
    print(len(comPipe.bufferTX), len(comPipe.bufferRX))
    if len(comPipe.bufferRX) > 0: comPipe.bufferRX.pop(0)
    sleep(0.01)
    
