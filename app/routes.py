from app import app
from flask import render_template, request
from app.models import model, formopener
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import Play, VoiceResponse
from app import addSong
import sys
import redis
import re
import random

account_sid = 'APf2f5f23cf6f056ee8076ffc651dff6dc'
auth_token = 'b48612d75f292e1fa4a719b6ebe547bd'
client = Client(account_sid, auth_token)
r = redis.Redis(host="localhost", port=6379)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/addPhoneNumber', methods=["GET"])
def addPhoneNumber():
    formattedPhoneNumber = re.sub('[^0-9]','', request.form["phone-number"])
    r.hset("numbers." + formattedPhoneNumber, "playlistURL", "None")
    message = client.messages \
                    .create(
                         body="Thank you for signing up. To set your playlist, send its YouTube link here.",
                         from_='+17343596043',
                         to="+1" + formattedPhoneNumber
                        )

@app.route("/receiveSms", methods=['GET', 'POST'])
def receiveSms():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    From = request.form["From"]
    Body = request.form["Body"]
    resp.message("Updating playlist to: " + Body)
    r.hset("numbers." + From, "playlistUrl", Body)
    # for kvp in request.form:
    #     print(kvp, file=sys.stderr)

@app.route("/reciveCall", methods=['GET' , 'POST'])
def reciveCall():
    numb = request.value["from"]
    if num[0] == '+':
        num = num[1:]
    print(num, file=sys.stderr)
    playlist = r.hget("numbers." + request.value["from"], "playlistUrl")
    if playlist is None: return
    player = addSong.MusicPlayer()
    player.addSongs(playlist, num)
    response = VoiceResponse()
    response.play(player.songNames, loop=10)
    print(response, file=sys.stderr)