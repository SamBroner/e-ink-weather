import os
from dotenv import load_dotenv
import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import requests

from layout import getBlack,getRed
import utils
from config import Ink_HEIGHT,Ink_WIDTH

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
imgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img')
logFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log.txt")

load_dotenv()

weather_key = os.getenv('WEATHER_KEY')
news_key = os.getenv('NEWS_KEY')
debug = os.getenv("DEBUG")

logging.basicConfig(filename=logFile,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(module)s... %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

def getImages():
    weatherJson = utils.getWeather(weather_key, "3")
    logging.info("Weather JSON Received")
    headlinesJson = utils.getHeadlines(news_key)
    
    redImg = getRed(weatherJson)
    blackImg = getBlack(weatherJson, headlinesJson)
    logging.info("Black Image Created")

    return (redImg, blackImg)

try:
    logging.info("Start E-Ink-Calendar")
    utils.makeImgDirIfNotExists()

    if bool(debug):
        logging.info("Running in DEBUG mode. Remove DEBUG from .env to run e-ink")

        (redImg, blackImg) = getImages()
        blackImg.save(os.path.join(imgdir, "black.png"))
        redImg.save(os.path.join(imgdir, "red.png"))
        blackImg.paste(redImg, (0, 0), blackImg)
        blackImg.save(os.path.join(imgdir, "full.png"))

    else:
        logging.info("Running on Raspberry Pi")
        from waveshare_epd import epd7in5b_HD

        epd = epd7in5b_HD.EPD()
        logging.info("init and Clear")
        epd.init()
        time.sleep(1)
        
        # My Drawings
        logging.info("Begin")
        weatherJson = utils.getWeather(weather_key, "3")

        blackImg = getBlack(weatherJson)
        redImg = getRed(weatherJson)
        logging.info("Red Image Created")

        epd.display(epd.getbuffer(blackImg), epd.getbuffer(redImg))
        time.sleep(2)

        logging.info("Goto Sleep...")
        epd.sleep()
        logging.info("Success")
        
except IOError as e:
    logging.error("IOError")
    logging.error(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_HD.epdconfig.module_exit()
    exit()

except:
    logging.error("Unidentified error")
    logging.error(traceback.format_exc())

logging.info("----------------------------------------------------------------------------------")