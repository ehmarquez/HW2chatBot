import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
import time
import keys

headers = keys.hw2key()

params = urllib.parse.urlencode({
})

def matchEvents(match):

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
    
    S1, tS1, P1, tP1, Exp1, timeX = ([] for i in range (6))
    S2, tS2, P2, tP2, Exp2 = ([] for i in range (5))
    Y1, Y2 = ([] for i in range(2))


    for i in events:

        if "PlayerIndex" and "HumanPlayerId" in i:
            list1.append(str(i["PlayerIndex"]))
            list2.append(i["HumanPlayerId"])    
            specID = dict(zip(list1,list2)) 
            
        if "PlayerResources" in i:
            resources = i["PlayerResources"]
            playerID1 = '1'
            playerID2 = '2'
            a = resources[playerID1]
            b = resources[playerID2]

            selectType = {
                1: 'TotalSupply',
                2: 'TotalEnergy',
                3: 'CommandXP'    
            }

            sel = 3

            Y1.append(a[selectType[sel]])
            Y2.append(b[selectType[sel]])

            S1.append(a['Supply'])
            tS1.append(a['TotalSupply'])
            P1.append(a['Energy'])
            tP1.append(a['TotalEnergy'])
            Exp1.append(a['CommandXP'])

            S2.append(b['Supply'])
            tS2.append(b['TotalSupply'])
            P2.append(b['Energy'])
            tP2.append(b['TotalEnergy'])
            Exp2.append(b['CommandXP'])


            xTime = (i['TimeSinceStartMilliseconds']/1000)
            timeX.append(xTime)

    import matplotlib.pyplot as plt
    import pylab

    plt.subplot(311)

    Player1 = specID[playerID1]['Gamertag']
    Player2 = specID[playerID2]['Gamertag']

    plt.plot(timeX, tS1, label=Player1)
    plt.plot(timeX, tS2, label=Player2)
    plt.ylabel('Total Supply')
    plt.xlabel('Time (s)')
    plt.legend()

    plt.subplot(312)
    plt.plot(timeX, tP1)
    plt.plot(timeX, tP2)
    
    plt.ylabel('Total Power')
    plt.xlabel('Time (s)')

    plt.subplot(313)
    plt.plot(timeX, Exp1)
    plt.plot(timeX, Exp2)
    plt.ylabel('Leader Point XP')
    plt.xlabel('Time (s)')

    pylab.savefig('stats.png')

    plt.gcf().clear()


            #supply = resources['Supply']
            #print (supply)

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
    from unitsConv import unitNames
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
            #   print('{} trained {} ({})'.format(playerName, squadID, mTime))

                
                
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

def matchRates(match):

    from numpy import diff

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
    
    S1, tS1, P1, tP1, Exp1, timeX = ([] for i in range (6))
    S2, tS2, P2, tP2, Exp2 = ([] for i in range (5))
    Y1, Y2, dy, dx = ([] for i in range(4))
    tech1, tech2 = ([] for i in range (2))


    for i in events:

        if "PlayerIndex" and "HumanPlayerId" in i:
            list1.append(str(i["PlayerIndex"]))
            list2.append(i["HumanPlayerId"])    
            specID = dict(zip(list1,list2)) 

        if "PlayerResources" in i:
            resources = i["PlayerResources"]
            playerID1 = '1'
            playerID2 = '2'
            a = resources[playerID1]
            b = resources[playerID2]

            selectType = {
                1: 'TotalSupply',
                2: 'TotalEnergy',
                3: 'CommandXP'    
            }

            sel = 3

            Y1.append(a[selectType[sel]])
            Y2.append(b[selectType[sel]])

            S1.append(a['Supply'])
            tS1.append(a['TotalSupply'])
            P1.append(a['Energy'])
            tP1.append(a['TotalEnergy'])
            Exp1.append(a['CommandXP'])
            tech1.append(a['TechLevel'])

            # Player 1 #
            # -------------------------- #
            # Player 2 #

            S2.append(b['Supply'])
            tS2.append(b['TotalSupply'])
            P2.append(b['Energy'])
            tP2.append(b['TotalEnergy'])
            Exp2.append(b['CommandXP'])
            tech2.append(b['TechLevel'])

            xTime = (i['TimeSinceStartMilliseconds']/1000)
            timeX.append(xTime) # Time Array

    import matplotlib.pyplot as plt
    import pylab
    import numpy as np

    v1 = np.array(tech1)
    T1 = np.where(v1[:-1] != v1[1:])[0]

    v2 = np.array(tech2)
    T2 = np.where(v2[:-1] != v2[1:])[0]

    ds2, ds2, dp1, dp2 = ([] for i in range(4))
    d1s, d2s, d1p, d2p = ([] for i in range (4))
    

    for z in timeX: # Rates of rates
        ds1 = diff(tS1)
        ds2 = diff(tS2)
        dp1 = diff(tP1)
        dp2 = diff(tP2)

        dx = diff(timeX)
   
        d1s = ds1/dx
        d2s = ds2/dx
        d1p = dp1/dx
        d2p = dp2/dx

    plt.style.use('ggplot')

    plt.subplot(221)

    Player1 = specID[playerID1]['Gamertag']
    Player2 = specID[playerID2]['Gamertag']

    plt.plot(timeX, S1, label=Player1)
    plt.plot(timeX, S2, label=Player2)
    plt.ylabel('Total Supply')
    plt.legend()

    plt.subplot(222)
    plt.plot(timeX, P1)
    plt.plot(timeX, P2)
    
    for i in T1:
        plt.axvline(timeX[i], linestyle='dotted', label='{} Tech Levelup'.format(Player1))

    for i in T2:
        plt.axvline(timeX[i], linestyle='dotted', label='{} Tech Levelup'.format(Player2))

    plt.ylabel('Total Power')
  
    del timeX[0]

    plt.subplot(223)
    plt.plot(timeX, d1s, label=Player1)
    plt.plot(timeX, d2s, label=Player2)
    plt.ylabel('Supply Income Rate')
    plt.xlabel('Time (s)')
   
    #plt.legend()

    plt.subplot(224)
    plt.plot(timeX, d1p, label=Player1)
    plt.plot(timeX, d2p, label=Player2)
    plt.ylabel('Power Income Rate')

    hline = int(plt.ylim()[1]/6)
    
    for j in range(hline):
        plt.axhline(6*(j+1), linestyle='dotted')
    
    plt.xlabel('Time (s)')
    #plt.legend()
    plt.gcf().set_size_inches(13.5,7.8)
    plt.subplots_adjust(bottom=0.1, top=0.95, right=0.97, left=0.07)
    pylab.savefig('rates.png')
    plt.gcf().clear()

def test(match):

    from numpy import diff

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
    
    S1, tS1, P1, tP1, Exp1, timeX, tech1= ([] for i in range (7))
    S2, tS2, P2, tP2, Exp2, tech2 = ([] for i in range (6))
    Y1, Y2, dy, dx = ([] for i in range(4))


    for i in events:

        if "PlayerIndex" and "HumanPlayerId" in i:
            list1.append(str(i["PlayerIndex"]))
            list2.append(i["HumanPlayerId"])    
            specID = dict(zip(list1,list2)) 

        if "PlayerResources" in i:
            resources = i["PlayerResources"]
            playerID1 = '1'
            playerID2 = '2'
            a = resources[playerID1]
            b = resources[playerID2]

            selectType = {
                1: 'TotalSupply',
                2: 'TotalEnergy',
                3: 'CommandXP'    
            }

            sel = 3

            Y1.append(a[selectType[sel]])
            Y2.append(b[selectType[sel]])

            S1.append(a['Supply'])
            tS1.append(a['TotalSupply'])
            P1.append(a['Energy'])
            tP1.append(a['TotalEnergy'])
            Exp1.append(a['CommandXP'])
            tech1.append(a['TechLevel'])

            # Player 1 #
            # -------------------------- #
            # Player 2 #

            S2.append(b['Supply'])
            tS2.append(b['TotalSupply'])
            P2.append(b['Energy'])
            tP2.append(b['TotalEnergy'])
            Exp2.append(b['CommandXP'])
            tech2.append(b['TechLevel'])

            xTime = (i['TimeSinceStartMilliseconds']/1000)
            timeX.append(xTime)

    import matplotlib.pyplot as plt
    import pylab
    import numpy as np

    v = np.array(tech1)
    V = np.where(v[:-1] != v[1:])[0]

    print (V)

    ds1, ds2, dp1, dp2 = ([] for i in range(4))
    d1s, d2s, d1p, d2p = ([] for i in range (4))
    
    plt.style.use('ggplot')
    plt.subplot(221)

    Player1 = specID[playerID1]['Gamertag']
    Player2 = specID[playerID2]['Gamertag']

    plt.plot(timeX, tech1, label=Player1)
    plt.plot(timeX, tech2, label=Player2)
    plt.ylabel('Tech Level')
    plt.legend()

    '''
    plt.subplot(222)
    plt.plot(timeX, P1)
    plt.plot(timeX, P2)
    plt.axhline(1500, linestyle='dotted')
    plt.axhline(1000, linestyle='dotted')
    plt.ylabel('Total Power')
    plt.xlabel('Time (s)')
    '''

    print(tech1)

    plt.gcf().set_size_inches(13.5,7.8)
    plt.subplots_adjust(bottom=0.1, top=0.95, right=0.97, left=0.07)
    pylab.savefig('test.png')
    plt.gcf().clear()

matchRates('a747b8ee-e081-4288-8cdb-73d17233c5bd')
            
#matchBuild('a747b8ee-e081-4288-8cdb-73d17233c5bd', 'TakeSomeNotess')
        


        

