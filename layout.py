import utils
from PIL import Image,ImageDraw,ImageFont
import os
import textwrap
import logging

from config import Ink_HEIGHT,Ink_WIDTH,main_Weather_Icon,small_Weather_Icon, today_x_start, tmrw_x_start, omrw_x_start

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
font42 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 42)

def getBlack(weatherJson):
    blackImg = generateImgOutline()
    currentWeatherIcon = utils.getWeatherIcon(weatherJson["current"], main_Weather_Icon)
    blackImg = generateBlackText(blackImg, weatherJson["current"])

    leftStart = round((Ink_WIDTH*2/3)/2 - main_Weather_Icon/2) # properly align the logo
    blackImg.paste(currentWeatherIcon, (leftStart, 100), currentWeatherIcon)

    blackImg = generateForecastWeatherText(blackImg, weatherJson)
    return blackImg

def getRed(weatherJson):
    redImg = utils.emptyImage()

    redImg = generateCurrentWeatherText(redImg, weatherJson["current"])

    todaysWeather = utils.getWeatherIcon(weatherJson["forecast"]["forecastday"][0]["day"], small_Weather_Icon)
    redImg.paste(todaysWeather, (today_x_start, round(Ink_HEIGHT * 2 / 3 + 5)), todaysWeather)

    tmrwsWeather = utils.getWeatherIcon(weatherJson["forecast"]["forecastday"][1]["day"], small_Weather_Icon)
    redImg.paste(tmrwsWeather, (tmrw_x_start, round(Ink_HEIGHT * 2 / 3 + 5)), tmrwsWeather)

    skipDayWeathers = utils.getWeatherIcon(weatherJson["forecast"]["forecastday"][2]["day"], small_Weather_Icon)
    redImg.paste(skipDayWeathers, (omrw_x_start, round(Ink_HEIGHT * 2 / 3 + 5)), skipDayWeathers)
    return redImg


def generateForecastWeatherText(img, weatherJson):
    todayHigh = round(weatherJson["forecast"]["forecastday"][0]["day"]["maxtemp_f"])
    todayLow = round(weatherJson["forecast"]["forecastday"][0]["day"]["mintemp_f"])

    tmrwHigh = round(weatherJson["forecast"]["forecastday"][1]["day"]["maxtemp_f"])
    tmrwLow = round(weatherJson["forecast"]["forecastday"][1]["day"]["mintemp_f"])

    day3High = round(weatherJson["forecast"]["forecastday"][2]["day"]["maxtemp_f"])
    day3Low = round(weatherJson["forecast"]["forecastday"][2]["day"]["mintemp_f"])

    drawImg = ImageDraw.Draw(img)
    drawImg.text((today_x_start + 13, round(Ink_HEIGHT * 2 / 3 + small_Weather_Icon + 5)), "{}˚- {}˚".format(todayHigh, todayLow), font = font20, fill = 0)
    drawImg.text((today_x_start + 19, round(Ink_HEIGHT * 2 / 3 + small_Weather_Icon + 28)), "Today".format(todayHigh, todayLow), font = font20, fill = 0)

    drawImg.text((tmrw_x_start + 13, round(Ink_HEIGHT * 2 / 3 + small_Weather_Icon + 5)), "{}˚- {}˚".format(tmrwHigh, tmrwLow), font = font20, fill = 0)
    drawImg.text((tmrw_x_start + 2, round(Ink_HEIGHT * 2 / 3 + small_Weather_Icon + 28)), "Tomorrow".format(tmrwHigh, tmrwLow), font = font20, fill = 0)

    drawImg.text((omrw_x_start + 13, round(Ink_HEIGHT * 2 / 3 + small_Weather_Icon + 5)), "{}˚- {}˚".format(day3High, day3Low), font = font20, fill = 0)
    drawImg.text((omrw_x_start - 6, round(Ink_HEIGHT * 2 / 3 + small_Weather_Icon + 28)), "Overmorrow".format(day3High, day3Low), font = font20, fill = 0)

    return img

def generateCurrentWeatherText(img, weatherReportJson):
    logging.info("generateCurrentWeatherText (RED)")
    drawImg = ImageDraw.Draw(img)
    drawImg.text((85, 10), "" + str(round(weatherReportJson["temp_f"])) + "˚", font = font36, fill = 0)

    description = utils.shortenWeatherText(weatherReportJson["condition"]["text"])
    drawImg.text((40, 60), "" + description , font = font36, fill = 0)

    logging.info("generateCurrentWeatherText created (RED)")

    return img

def generateImgOutline():
    blackImg = utils.emptyImage()
    drawBlackImg = ImageDraw.Draw(blackImg)
    drawBlackImg.line((round(Ink_WIDTH*2/3), 0, Ink_WIDTH*2/3, Ink_HEIGHT ))
    drawBlackImg.line((0, Ink_HEIGHT * 2/3, Ink_WIDTH*2/3, Ink_HEIGHT*2/3))

    return blackImg

# todo: fix this mess
def generateBlackText(blackImg, weatherReportJson):
    logging.info("GenerateBlackText")
    drawBlackImg = ImageDraw.Draw(blackImg)
    drawBlackImg.text((10, 15), 'Hi, it\'s ', font = font24, fill = 0)
    drawBlackImg.text((150, 15), utils.getUniqueInfo(weatherReportJson), font = font24, fill = 0)

    drawBlackImg.text((10, 60), '... ', font = font24, fill = 0)

    logging.info("Create Headlines")
    headlines = utils.getHeadlines()

    lines = []
    i = 0
    while len(lines) < 22 and i != -1:
        newlines = (textwrap.wrap("#  " + headlines[i]["title"], width=29))
        if len(lines) + len(newlines) < 22:
            lines  = lines + newlines
            lines = lines + [" "]
            i += 1
        else:
            i = -1

    text = ""
    for line in lines:
        text += line + "\n"

    drawBlackImg.text(((round(Ink_WIDTH*2/3) + 40), 5), "Headlines", fill=0, font=font24)

    drawBlackImg.multiline_text(((round(Ink_WIDTH*2/3) + 5), 40), text, fill=0, font=font20)

    logging.info("Black Text Finished")

    return blackImg