import json
from channels import Channel, Group
from channels.auth import channel_session_user_from_http, channel_session_user

### WebSocket handling ###


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    userid = str(message.user)
    message.reply_channel.send({'accept': True})
    Group('chat'+userid).add(message.reply_channel)
    Group('chat').add(message.reply_channel)
    #sendall = {'command':'joined', 'username':userid}
    #m = {'text': json.dumps(sendall)}
    #Group('chat').send(m)


# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)
def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    if "join" in payload.values() or "joined" in payload.values():
        Channel("chat.receive").send(payload)
    if "send" in payload.values():
        Channel("chat.receive").send(payload)


@channel_session_user
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    pass


### Chat channel handling ###


# Channel_session_user loads the user out from the channel session and presents
# it as message.user. There's also a http_session_user if you want to do this on
# a low-level HTTP handler, or just channel_session if all you want is the
# message.channel_session object without the auth fetching overhead.
@channel_session_user
def chat_join(message):
    # Find the room they requested (by ID) and add ourselves to the send group
    # Note that, because of channel_session_user, we have a message.user
    # object that works just like request.user would. Security!
    sendall = {'command': 'joined', 'username': message.content['username']}
    m = {'text': json.dumps(message.content)}
    Group('chat').send(m, immediately=True)


@channel_session_user
def chat_leave(message):
    userid = message.content['username']
    Group("chat").discard(message.reply_channel)
    Group("chat"+userid).discard(message.reply_channel)


@channel_session_user
def chat_send(message):
    # Check that the user in the room
    userid = message.content['send_to']
    m = {'text': json.dumps(message.content)}
    Group('chat'+userid).send(m)
    #Group('chat').send({'text': json.dumps(m)})
