# JU NaOv6 DEMO, developed by the Laboratory of applied development and research
# coding=utf-8
import os.path
import time

import naoGrpcSpeechServer
import naoSpeech
import naoVoiceRecognition
import naoPosture
import naoPlaySound
import naoDance
import naoLeds
import naoLife
import naoMove
import naoCam

def naoDemonstration(ip, port, treshold, timeOut, volume, walkTimeout, walkSpeed, maxSteps = 10):
    # speech / talking
    ns = naoSpeech.naoSpeech(ip, port)
    ns.setVolume(volume)

    #######
    # naoCam

    # init
    nl = naoLeds.naoLeds(ip, port)
    np = naoPosture.naoPosture(ip, port)
    nlf = naoLife.naoLife(ip, port)

    # initiating
    nl.processingOff()
    time.sleep(0.5)

    ## posture correction
    np.sitDown()

    ## moving off
    nlf.movingOff()
    nlf.pauseMotion()

    ## processing on
    ns.sayText("Capturing face in 3, 2, 1!")
    nl.processingOn()

    # camera commands
    nc = naoCam.naoCam(ip, port)
    nc.get_images()
    ns.sayText("Processing your image, please wait")

    # say response
    response = nc.get_response()
    ns.sayText(str(response))

    # close
    nl.processingOff()
    nlf.movingOn()
    nlf.resumeMotion()
    ######

def naoChatBot(ip, port, volume):
    ns = naoSpeech.naoSpeech(ip, port)
    ns.setVolume(volume)
    nl = naoLeds.naoLeds(ip, port)
    nl.recognizeOn()
    print("Pripraven.")
    naoGrpcSpeechServer.serve(ns, nl)

# connection & other params
ip = "IP"
port = "PORT"
treshold = 0.4
timeOut = 7
volume = 1
walkSpeed = 0.4
walkTimeout = 2
maxSteps = 5

# start demonstration
naoDemonstration(ip, port, treshold, timeOut, volume, walkTimeout, walkSpeed, maxSteps)
#naoChatBot(ip, port, volume)
