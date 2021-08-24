import requests, random, subprocess, os, sys

# Put your cookies in a file cookies.txt and separate with a new line (enter).
with open('cookies.txt', 'r') as cookies:
    cookies = cookies.read().splitlines()

# Want to use a specific cookie? Edit the line below.
# Example 1: cookie = "_|WARNING:DO-NOT-SHARE-THIS....."
# Example 2: cookies = str(input("Input cookie (starts with _|WARNING:)\n"))
cookie = random.choice(cookies)
gameid = int(input("Input game ID\n"))

# Please do not edit beyond this point unless you know what you're doing.
def get_immediate_subdirectories(a_dir):
	return [name for name in os.listdir(a_dir)
		if os.path.isdir(os.path.join(a_dir, name))]

versionsPath = os.getenv("LOCALAPPDATA") + "/Roblox/Versions";
try:
	dirNames = get_immediate_subdirectories(versionsPath);
except FileNotFoundError:
	print("Could not locate any versions of Roblox. Please make sure it's installed.");
	sys.exit(1);

dirNames.sort(key=lambda n: -int(n.split("-")[1], 16));

if(len(dirNames) < 1):
	print("Could not locate any versions of Roblox. Please make sure it's installed.");
	sys.exit(1);

print(dirNames);

robloxPath = versionsPath + "/" + dirNames[0];

def getAuthTicket():
    with requests.session() as session:
        session.cookies['.ROBLOSECURITY'] = cookie
        session.headers['x-csrf-token'] = session.post('https://accountsettings.roblox.com/v1/email').headers['x-csrf-token']
        session.headers['origin'] = 'https://www.roblox.com'
        session.headers['referer'] = 'https://www.roblox.com/'
        authTicketReq = session.post('https://auth.roblox.com/v1/authentication-ticket/')
        authTicket = authTicketReq.headers['rbx-authentication-ticket']
        return authTicket

def joinGame(auth):
    try:
        print('Launching game...')
        subprocess.call("\"%(path)s/RobloxPlayerBeta.exe\" --play -a https://www.roblox.com/Login/Negotiate.ashx -t %(ticket)s -j https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId=%(browserTracker)i&placeId=%(placeId)i&isPartyLeader=false -b %(browserTracker)i" % {"path": robloxPath, "ticket": auth, "placeId": gameid, "browserTracker": random.randint(1111111, 9999999)})
        print("Game closed.")
    except:
        print('There was an error while launching Roblox.')

joinGame(getAuthTicket())