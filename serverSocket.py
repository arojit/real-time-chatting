from aiohttp import web
import socketio

# creates a new Async Socket IO Server
sio = socketio.AsyncServer()
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

# we can define aiohttp endpoints just as we normally
# would with no change
async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the
# event we wish to listen out for
@sio.on('userMessage')
async def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message   
    await sio.emit('message', message["message"],user[message["sendTo"]]["socketId"])

@sio.on('acceptRequest')
async def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message   
    await sio.emit('acceptRequest', message,user[message["sendTo"]]["socketId"])

@sio.on('agentMessage')
async def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message   
    await sio.emit('message', message["message"],agent[message["sendTo"]]["socketId"])

agent = {}
@sio.on('AgentJoin')
async def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
    
    print("-----Agent Join -------")
    agent[message["userID"]] = {"socketId": sid, "domain": message["domain"]}
    print(agent,"\n---------------")
    
    await sio.emit('AgentJoin', "Connected to Socket",sid)

user = {}
@sio.on('UserJoin')
async def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
 
    print("-----User Join -------")
    user[message["userID"]] = {"socketId": sid, "domain": message["domain"]}
    print(user,"\n---------------")
    msg = {"message": "You've a request", "from": message["userID"]}
    for key in agent:
        if(agent[key]["domain"] == message["domain"]):
            await sio.emit("chatRequest",msg,agent[key]["socketId"])

    await sio.emit('UserJoin', "Connected to Socket",sid)
# We bind our aiohttp endpoint to our app
# router
app.router.add_get('/', index)

# We kick off our server
if __name__ == '__main__':
    web.run_app(app)