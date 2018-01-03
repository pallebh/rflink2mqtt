import logging.handlers

def createLogger( nane ) :
    logger = logging.getLogger( __name__ )

    logger.setLevel( logging.INFO )
    logFile = logging.handlers.RotatingFileHandler( "/var/log/rlink2mqtt.log" , mode = "a", maxBytes = 1024*1024 , backupCount = 5  )
    slogFile.setLevel( logging.DEBUG )

    formatter = logging.Formatter("%(name)s:%(lineno)d %(asctime)s;%(levelname)s;%(message)s" , datefmt='%m/%d/%Y %H:%M:%S' )
    logFile.setFormatter(formatter)
    logger.addHandler( logFile )

    logConsole = logging.StreamHandler()
    logConsole.setLevel( logging.DEBUG )
    logConsole.setFormatter(formatter)
    logger.addHandler( logConsole )
    
    return logger
