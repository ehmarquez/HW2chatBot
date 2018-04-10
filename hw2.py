import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
import time
import keys
from numpy import around
from numpy import diff
from unitsConv import unitNames
import matplotlib.pyplot as plt
import numpy as np
import pylab
from collections import OrderedDict    


# pull key from key.py
headers = keys.hw2key()

params = urllib.parse.urlencode({
})

def rnd(arr):
    for i in arr:
        i = around(i)

def matchBuild(match, gameTag):
    
    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", "/stats/hw2/matches/{}/events?%s".format(match) % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    jsondata = json.loads(data)
    jsonkeys = jsondata.keys()
    jsonvalues = jsondata.values()
    jsonitems = jsondata.items()

    # jsondata['GameEvents']

    events = (jsondata["GameEvents"])

    # events = matchevent API data
    # i = sets of events

    print (len(events))

    list1 = []
    list2 = []

    # Metadata names to Real
    unitConv = unitNames()
    Names = []
    
    for i in events:
        
        if "PlayerIndex" and "HumanPlayerId" in i:
            list1.append(str(i["PlayerIndex"]))
            list2.append(i["HumanPlayerId"])    
            specID = dict(zip(list1,list2)) 

        if "PlayerIndex" and "SquadId" in i:
            playerID = str(i["PlayerIndex"])
            playerName = specID[playerID]['Gamertag']

            if playerName not in Names:
                Names.append(playerName)

            squadID = i["SquadId"]
            timeint = i['TimeSinceStartMilliseconds'] / 1000
            mTime = time.strftime("%M:%S", time.gmtime(timeint))

    fileobj = open('build.txt','w')
    
    for i in events:

        if "PlayerIndex" and "HumanPlayerId" in i:
            list1.append(str(i["PlayerIndex"]))
            list2.append(i["HumanPlayerId"])    
            specID = dict(zip(list1,list2)) 

        if "PlayerIndex" and "SquadId" in i:
            playerID = str(i["PlayerIndex"])
            playerName = specID[playerID]['Gamertag']
            squadID = i["SquadId"]
            timeint = i['TimeSinceStartMilliseconds'] / 1000
            mTime = time.strftime("%M:%S", time.gmtime(timeint))

            if playerName == gameTag:
                for k, v in unitConv.items():
                    if squadID == k:
                        squadID = v             
                fileobj.write('{} trained {} ({})\n'.format(playerName, squadID, mTime))
                print('{} trained {} ({})'.format(playerName, squadID, mTime))

            elif gameTag not in Names:
                print('Invalid Gamertag. Gametag: ({})'.format(gameTag))
                print(Names)
                return False
    
    fileobj.close()

    with open('build.txt', 'r') as file1:
        text = file1.read().strip().split()
        len_chars = sum(len(word) for word in text)
        print(len_chars)

        if len_chars < 1900:
            return True

    return False

# shows supply/power income of a game provided a matchID from halo waypoint match history URL
def matchRates(match): 
    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", "/stats/hw2/matches/{}/events?%s".format(match) % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    jsondata = json.loads(data)
    jsonkeys = jsondata.keys()
    jsonvalues = jsondata.values()
    jsonitems = jsondata.items()

    events = (jsondata["GameEvents"])

    # events = matchevent API data
    # i = sets of events

    print (len(events))

    list1 = []
    list2 = []
    
    # initialize lists for plotting    
    S1, tS1, P1, tP1, Exp1, pop1, popcap1 ,timeX = ([] for i in range (8))
    S2, tS2, P2, tP2, Exp2, pop2, popcap2 = ([] for i in range (7))
    Y1, Y2, dy, dx = ([] for i in range(4))
    tech1, tech2 = ([] for i in range (2))

    counter = 0

    for i in events:

        # map playerID to Gamertag
        if "PlayerIndex" and "HumanPlayerId" in i:
            list1.append(str(i["PlayerIndex"]))
            list2.append(i["HumanPlayerId"])    
            specID = dict(zip(list1,list2)) 

        # parse "PlayerResources" data from HW2 API    
        if "PlayerResources" in i:

            counter = counter + 1

            resources = i["PlayerResources"]
            playerID1 = '1'
            playerID2 = '2'
            a = resources[playerID1]
            b = resources[playerID2]

            ''' # selection dictionary
            selectType = {
                1: 'TotalSupply',
                2: 'TotalEnergy',
                3: 'CommandXP'    
            }

            sel = 3

            Y1.append(a[selectType[sel]])
            Y2.append(b[selectType[sel]])
            '''

            S1.append(a['Supply'])
            tS1.append(a['TotalSupply'])
            P1.append(a['Energy'])
            tP1.append(a['TotalEnergy'])
            Exp1.append(a['CommandXP'])
            tech1.append(a['TechLevel'])
            #pop1.append(a['Population'])
            #popcap1.append(a['PopulationCap'])

            # Player 1 #
            # -------------------------- #
            # Player 2 #

            S2.append(b['Supply'])
            tS2.append(b['TotalSupply'])
            P2.append(b['Energy'])
            tP2.append(b['TotalEnergy'])
            Exp2.append(b['CommandXP'])
            tech2.append(b['TechLevel'])
            #pop2.append(b['Population'])
            #popcap2.append(b['PopulationCap'])

            xTime = (i['TimeSinceStartMilliseconds']/1000)
            timeX.append(xTime) # Time Array

    print ('Resource heartbeat count: {}'.format(counter))

    # search for Tech level changes 
    v1 = np.array(tech1)
    T1 = np.where(v1[:-1] != v1[1:])[0]
    v2 = np.array(tech2)
    T2 = np.where(v2[:-1] != v2[1:])[0]

    
    ds2, ds2, dp1, dp2 = ([] for i in range(4))
    
    # dy/dx of supply/power
    d1s, d2s, d1p, d2p = ([] for i in range (4))
    
    for z in timeX: # Rates of rates
        
        dx = diff(timeX)
        d1s = diff(tS1)/dx
        d2s = diff(tS2)/dx
        d1p = diff(tP1)/dx
        d2p = diff(tP2)/dx

    def round_down(num, divisor):
        return num - (num%divisor)
    
    def rarray(arr):
        temp = []
        for i in arr:
            temp.append(round_down(i,0.01))
        return temp    

    d1s = d1s.tolist()
    d1s = rarray(d1s)
    d2s = rarray(d2s)
    d1p = rarray(d1p)
    d2p = rarray(d2p)

    plt.style.use('ggplot')

    # Plot 1 (current supply)
    
    Player1 = specID[playerID1]['Gamertag']
    Player2 = specID[playerID2]['Gamertag']

    del timeX[0]

    # supply income rate (supply/s)
    plt.subplot(121)
    plt.plot(timeX, d1s, label=Player1)
    plt.plot(timeX, d2s, label=Player2)
    plt.ylabel('Supply Income Rate (supply/s)')
    plt.xlabel('Time (s)')
   
    #power income rate (power/s)
    #included markers for adv. generator intervals (every 6power/s/s)
    plt.subplot(122)
    plt.plot(timeX, d1p)
    plt.plot(timeX, d2p)
    plt.ylabel('Power Income Rate (power/s)')
    plt.xlabel('Time (s)')

    # lines marking when tech level was upgraded
    for i in T1:
        plt.axvline(x=timeX[i], linestyle='dashed', label='{} Tech Levelup'.format(Player1), c='r', ymax = 0.2) 
    for i in T2:
        plt.axvline(x=timeX[i], linestyle='dashed', label='{} Tech Levelup'.format(Player2), c='b', ymax = 0.2)

    hline = int(plt.ylim()[1]/6)

    for j in range(hline):
        plt.axhline(6*(j+1), linestyle='-', c='black', label='Adv. Generator Count', xmax = 0.52, xmin = 0.48)

    handles, labels = plt.gca().get_legend_handles_labels()

    # format legend
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.gcf().set_size_inches(14,5)

    plt.subplots_adjust(bottom=0.1, top=0.95, right=0.97, left=0.07) # Padding values

    pylab.savefig('rates.png')
    plt.gcf().clear()

# scatter plots units deaths and buildings queued
def deathmap(match):
    
    def coords(ddict):
        x,y,z = ([] for i in range(3))
        for i in range(len(ddict)):
            x.append(ddict[i]['x'])
            y.append(ddict[i]['y'])
            z.append(ddict[i]['z'])

        return x,y,z


    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", "/stats/hw2/matches/{}/events?%s".format(match) % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    jsondata = json.loads(data)
    jsonkeys = jsondata.keys()
    jsonvalues = jsondata.values()
    jsonitems = jsondata.items()

    events = (jsondata["GameEvents"])
    list1, list2, death1, death2, b1 = ([] for i in range(5))
    
    for i in events:
    
        if "PlayerIndex" and "HumanPlayerId" in i:
            list1.append(str(i["PlayerIndex"]))
            list2.append(i["HumanPlayerId"])    
            specID = dict(zip(list1,list2)) 
        
        if i["EventName"] == 'BuildingConstructionQueued':
            A = i['Location']
            b1.append(A)
            
        if i['EventName'] == 'Death':
            a = i['VictimLocation']
            b = str(i['VictimPlayerIndex'])
            player = specID[b]
            
            if b == '1':
                death1.append(a)
            else:
                death2.append(a)

    x1, y1, z1 = coords(death1)
    x2, y2, z2 = coords(death2)
    x3, y3, z3 = coords(b1)
    
    fig = plt.figure()
    ax = fig.gca()

    plt.style.use('ggplot')
    
    ax.scatter(z1,x1, c='r') # player 1 deaths
    ax.scatter(z2,x2, c='b') # player 2 deaths
    ax.scatter(z3, x3, c='g') # buildings queued

    plt.show()

# using Match Events endpoint:
# displays every unit death/what killed it
# incomplete 
def death(match):
    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", "/stats/hw2/matches/{}/events?%s".format(match) % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    jsondata = json.loads(data)
    jsonkeys = jsondata.keys()
    jsonvalues = jsondata.values()
    jsonitems = jsondata.items()

    events = (jsondata["GameEvents"])

    conv = unitNames()
    print(conv)

    for i in events:
        if i['EventName'] == 'Death':
            unitName = i['VictimObjectTypeId']
            unitIns = i['VictimInstanceId']
            a = i['Participants']
            strlist = []
            for k, v in a.items():
                b = a[k]['ObjectParticipants']
                for k1 in b.items():
                    murderer = k1[0]
                    
                    for k,v in conv.items():
                        if unitName == k:
                            unitName = v
                        elif murderer == k:
                            murderer = v 

                    specs = k1[1]
                    count = specs['Count']
                    dmg = specs['CombatStats']
                    for k2 in dmg:
                        v2 = dmg[k2]['AttacksLanded']
                        strlist.append('\n{} {}. DAMAGE: (ID: {} | AttacksLanded: {}'.format(count, murderer, k2, v2))

                    for i in strlist:
                        print('{} killed by {}'.format(unitName, i))
                        #print ('{} killed by {} {}. DAMAGE: (ID: {} | AttacksLanded: {})'.format(unitName, count, murderer, k2, v2))

                    #print(dmg)

# MMR throughout past 10 1v1 X games
def mmr(gamertag):

    reqgamertag = gamertag.replace(' ', '+')
    print ('{} and {}'.format(gamertag, reqgamertag))

    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", "/stats/hw2/players/{}/matches?%s".format(reqgamertag) % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
       # print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    jsondata = json.loads(data)
    jsonkeys = jsondata.keys()
    jsonvalues = jsondata.values()
    jsonitems = jsondata.items()

    # using Match History endpoint
    results = jsondata['Results']

    mmrhist = []
    count = []
    counter = 0

    for i in results:
        # 1v1 crossplay playlist ID
        if i['PlaylistId'] == '548d864e-8666-430e-9140-8dd2ad8fbfcd' and counter < 10: 
            a = i['RatingProgress']
            b = a['UpdatedMmr']['Rating']
            b = around(b,3)
            mmrhist.append(b)
            counter = counter + 1
            count.append(counter)
        
    plt.style.use('ggplot')

    
    mmrhist = mmrhist[::-1]
    # print ('{}\n{}'.format(mmrhist, count))
    plt.plot(count, mmrhist, marker='.')

    # Annotations
    for i, txt in enumerate(mmrhist):
        plt.annotate(txt, (count[i],mmrhist[i]+0.05))

    # Title
    plt.title('{} MMR history'.format(gamertag))

    # additional formatting
    plt.gca().set_ylim(min(mmrhist)-0.5, max(mmrhist)+0.5)

    pylab.savefig('mmr.png')
    plt.gcf().clear()

#mmr('MY TV TURNEDOFF')
#346634df-1d7f-4b14-b8d0-ba7d80e6f65f
#matchRates('346634df-1d7f-4b14-b8d0-ba7d80e6f65f')     
#deathmap('346634df-1d7f-4b14-b8d0-ba7d80e6f65f')           
#death('346634df-1d7f-4b14-b8d0-ba7d80e6f65f')           
#matchBuild('a747b8ee-e081-4288-8cdb-73d17233c5bd', 'TakeSomeNotess') 

# 1v1 X ID: 548d864e-8666-430e-9140-8dd2ad8fbfcd


        

