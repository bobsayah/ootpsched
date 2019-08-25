from collections import namedtuple
from datetime import date
from datetime import timedelta
from collections import namedtuple
import calendar
import random

year=1961
mlbdivisions = ['American', 'National', 'Western']
teams = { 'American' : ['NYY', 'BAL', 'BOS', 'CLE', 'WAS', 'DET'],
          'National' : ['BKN', 'PIT', 'MIL', 'CIN', 'PHI', 'CHI'],
          'Western' : ['STL', 'COL', 'DAL', 'LA', 'KC', 'SF'],
        }

seriesdates = namedtuple('seriesdates', 'startdate, length, datetype, serieslist')
series = namedtuple('series', 'seriestype homediv awaydiv numgames seriesnum reversed')
matchup = namedtuple('matchup', 'home away')
gameday = namedtuple('date', 'gamelist')
game = namedtuple('home', 'away')

def openingday(year):
    startdate=date(year,4,7)
    startdate=startdate+timedelta(4-startdate.weekday())
    return startdate
    
def isaholiday(mydate):

    memorialday=calendar.Calendar().monthdatescalendar(year,5)[-1][0]
    fourthofjuly=date(year,7,4)
    laborday=calendar.Calendar().monthdatescalendar(year,9)[1][0]

    if mydate == memorialday:
        return 1
    elif mydate == fourthofjuly:
        return 1
    elif mydate == laborday:
        return 1
    elif mydate == openingday(mydate.year):
        return 1
    else:
        return 0

def initializeseriesdates():

    dates=[]
    currentdate=openingday(year)
    dates.append(seriesdates(currentdate,3,'holiday',[]))
    currentdate=currentdate+timedelta(3)

    for w in range(0,24):
        if currentdate.weekday() == 1:
            dates.append(seriesdates(currentdate,3,'weekday',[]))
            currentdate=currentdate+timedelta(3)
            dates.append(seriesdates(currentdate,3,'weekend',[]))
            currentdate=currentdate+timedelta(3)
        elif isaholiday(currentdate+timedelta(7)):
            dates.append(seriesdates(currentdate,4,'weekday',[]))
            currentdate=currentdate+timedelta(4)
            dates.append(seriesdates(currentdate,4,'holiday',[]))
            currentdate=currentdate+timedelta(4)
        else:
            dates.append(seriesdates(currentdate,3,'weekday',[]))
            currentdate=currentdate+timedelta(3)
            dates.append(seriesdates(currentdate,4,'weekend',[]))
            currentdate=currentdate+timedelta(4)
    return dates

def initializematchups():
    
    matchups=dict()
    matchups['roundrobin'] = [[matchup(1,2),matchup(3,4),matchup(5,0)],
                [matchup(2,3),matchup(4,5),matchup(0,1)],
                [matchup(1,5),matchup(2,4),matchup(0,3)],
                [matchup(3,1),matchup(4,0),matchup(5,2)],
                [matchup(1,4),matchup(3,5),matchup(0,2)]
                ]
    matchups['divdiv'] = [[matchup(1,1),matchup(2,2),matchup(3,3),matchup(4,4),matchup(5,5),matchup(0,0)],
                            [matchup(1,2),matchup(2,3),matchup(3,4),matchup(4,5),matchup(5,0),matchup(0,1)],
                            [matchup(1,3),matchup(2,4),matchup(3,5),matchup(4,0),matchup(5,1),matchup(0,2)],
                            [matchup(1,4),matchup(2,5),matchup(3,0),matchup(4,1),matchup(5,2),matchup(0,3)],
                            [matchup(1,5),matchup(2,0),matchup(3,1),matchup(4,2),matchup(5,3),matchup(0,4)],
                            [matchup(1,0),matchup(2,1),matchup(3,2),matchup(4,3),matchup(5,4),matchup(0,5)]
            ]
    return matchups

def initializeseries():
    allseries = []
    allseries = allseries + [ series('divdiv','National','American',4,n,0) for n in range(0,len(matchups['divdiv']))]
    allseries = allseries + [ series('divdiv','American','Western',4,n,0) for n in range(0,len(matchups['divdiv']))]
    allseries = allseries + [ series('divdiv','Western','National',4,n,0) for n in range(0,len(matchups['divdiv']))]
    allseries = allseries + [ series('divdiv','National','American',3,n,1) for n in range(0,len(matchups['divdiv']))]
    allseries = allseries + [ series('divdiv','American','Western',3,n,1) for n in range(0,len(matchups['divdiv']))]
    allseries = allseries + [ series('divdiv','Western','National',3,n,1) for n in range(0,len(matchups['divdiv']))]

    allseries = allseries + [ series('roundrobin',div,div,4,n,0) for div in mlbdivisions for n in range(0,len(matchups['roundrobin']))]
    allseries = allseries + [ series('roundrobin',div,div,3,n,0) for div in mlbdivisions for n in range(0,len(matchups['roundrobin']))]
    allseries = allseries + [ series('roundrobin',div,div,3,n,1) for div in mlbdivisions for n in range(0,len(matchups['roundrobin']))]
    allseries = allseries + [ series('roundrobin',div,div,2,n,1) for div in mlbdivisions for n in range(0,len(matchups['roundrobin']))]
    allseries = allseries + [ series('roundrobin',div,div,2,n,1) for div in mlbdivisions for n in range(0,len(matchups['roundrobin']))]
    random.shuffle(allseries)
    return allseries

def printall(all):
    for s in all:
        print(s)

def poproundrobinseriesexact(allseries,division,numgames):
    for s in allseries:
        if s.seriestype == 'roundrobin' and s.homediv == division and s.numgames == numgames:
            allseries.remove(s)
            return s
    raise

def poproundrobinseriesmin(allseries,division,numgames):
    for s in allseries:
        if s.seriestype == 'roundrobin' and s.homediv == division and s.numgames >= numgames:
            allseries.remove(s)
            return s
    raise
    
def popdivdivseries(allseries,numgames,blackout='NoBlackout'):
    for s in allseries:
        if s.seriestype == 'divdiv' and s.numgames == numgames and s.homediv != blackout and s.awaydiv != blackout:
            allseries.remove(s)
            return s
    raise

def assignholidayseries(dates,series):
    for d in dates:
        if d.datetype == 'holiday':
            for div in mlbdivisions:
                d.serieslist.append(poproundrobinseriesexact(series,div,d.length))

def assignfourgamedivdiv(dates,series):
    for d in dates:
        if len(d.serieslist):
            continue
        if d.length == 4 and d.datetype == 'weekend':
            try:
                divdivseries = popdivdivseries(series,4)
            except:
                return None
            d.serieslist.append(divdivseries)
            divlist = mlbdivisions.copy()
            divlist.remove(divdivseries.homediv)
            divlist.remove(divdivseries.awaydiv)
            d.serieslist.append(poproundrobinseriesexact(series,divlist[0],3))

# To spread out the days off, we try to avoid scheduling a divdiv series
# for the same division three times in a row.
def search_for_blackout_div(datesbefore,datesafter):
    divisions_playing = set()
    for s in datesbefore.serieslist:
        if s.seriestype == 'divdiv':
            divisions_playing.add(s.homediv)
            divisions_playing.add(s.awaydiv)
    for s in datesafter.serieslist:
        if s.seriestype == 'divdiv':
            if s.homediv in divisions_playing:
                return s.homediv
            if s.awaydiv in divisions_playing:
                return s.awaydiv
    return 'NoBlackout'
    

def assignthreegamedivdiv(dates,series):
    for r in range(0,len(dates)):
        d = dates[r]
        if not len(d.serieslist) and d.length >= 3:
            if r in range(1,len(dates)-1):
                blackout = search_for_blackout_div(dates[r-1],dates[r+1])
            else:
                blackout = 'NoBlackout'
            try:
                divdivseries = popdivdivseries(series,3,blackout)
            except:
                try:
                    divdivseries = popdivdivseries(series,3)
                except:
                    return None
            d.serieslist.append(divdivseries)
            divlist = mlbdivisions.copy()
            divlist.remove(divdivseries.homediv)
            divlist.remove(divdivseries.awaydiv)
            if d.datetype == 'weekend':
                if d.length == 3:
                    d.serieslist.append(poproundrobinseriesexact(series,divlist[0],3))
                else:
                    d.serieslist.append(poproundrobinseriesmin(series,divlist[0],3))
            else:
                d.serieslist.append(poproundrobinseriesexact(series,divlist[0],2))

def assignfourgameroundrobin(dates,series):
    for d in dates:
        if len(d.serieslist):
            continue
        if d.length == 4:
            try:
                series1=poproundrobinseriesexact(series,mlbdivisions[0],4)
            except:
                series1=poproundrobinseriesexact(series,mlbdivisions[0],3)
            try:
                series2=poproundrobinseriesexact(series,mlbdivisions[1],4)
            except:
                series2=poproundrobinseriesexact(series,mlbdivisions[1],3)
            try:
                series3=poproundrobinseriesexact(series,mlbdivisions[2],4)
            except:
                series3=poproundrobinseriesexact(series,mlbdivisions[2],3)
            d.serieslist.append(series1)
            d.serieslist.append(series2)
            d.serieslist.append(series3)

def assignthreegameweekendroundrobin(dates,series):
    for d in dates:
        if len(d.serieslist):
            continue
        if d.length == 3 and d.datetype == 'weekend':
            d.serieslist.append(poproundrobinseriesexact(series,mlbdivisions[0],3))
            d.serieslist.append(poproundrobinseriesexact(series,mlbdivisions[1],3))
            d.serieslist.append(poproundrobinseriesexact(series,mlbdivisions[2],3))

def assignthreegameweekdayroundrobin(dates,series):
    for d in dates:
        if len(d.serieslist):
            continue
        if d.length == 3 and d.datetype == 'weekday':
            try:
                d.serieslist.append(poproundrobinseriesmin(series,mlbdivisions[0],2))
                d.serieslist.append(poproundrobinseriesmin(series,mlbdivisions[1],2))
                d.serieslist.append(poproundrobinseriesmin(series,mlbdivisions[2],2))
            except:
                raise

def countseries(dates,series):
    assignedcount=0
    unassigneddates=0
    for d in dates:
        if (len(d.serieslist)):
            assignedcount=assignedcount+len(d.serieslist)
        else:
            unassigneddates+=1
    print(str(assignedcount)+' series have been assigned')
    unassignedcount=len(series)
    print(str(unassignedcount)+' series are still unassigned')
    print('Total is '+str(assignedcount+unassignedcount))
    print(str(unassigneddates)+' dates are unassigned')
    

def swap_series(allseriesdates,replacementdate,replacementseries):
    randlist = list(range(0,len(allseriesdates)))
    random.shuffle(randlist)
    for r in randlist:
        seriesdate = allseriesdates[r]
        if abs(seriesdate.startdate-replacementdate.startdate).days < 10:
            continue
        if seriesdate.datetype != replacementdate.datetype:
            continue
        for i in seriesdate.serieslist:
            if ( i.homediv == replacementseries.homediv and
                 i.awaydiv == replacementseries.awaydiv and
                 i.seriesnum != replacementseries.seriesnum and
                 i.seriestype == replacementseries.seriestype and
                 seriesdate.length >= replacementseries.numgames and
                 replacementdate.length >= i.numgames):
                print("replacement series:"+str(seriesdate.startdate)+':'+str(replacementseries))
                seriesdate.serieslist.remove(i)
                replacementdate.serieslist.remove(replacementseries)
                seriesdate.serieslist.append(replacementseries)
                replacementdate.serieslist.append(i)
                return
    print('ERROR')
    print('Could not find a series to swap with:')
    print(replacementseries)
    exit(1)


def rearrange_series(allseriesdates):
    something_rearranged = False
    for r in range(1,len(allseriesdates)):
        earlier = allseriesdates[r-1]
        later = allseriesdates[r]
        for i in earlier.serieslist:
            for j in later.serieslist:
                if ( i.seriestype == j.seriestype and
                     ((i.homediv == j.homediv and i.awaydiv == j.awaydiv) or (i.homediv == j.awaydiv and i.awaydiv == j.homediv)) and
                     i.seriesnum == j.seriesnum):
                    print('Two consecutive series between same sets of teams:'+str(earlier.startdate)+':'+str(later.startdate))
                    print(earlier)
                    print(later)
                    swap_series(allseriesdates,earlier,i)
                    print('After replacement')
                    print(earlier)
                    print(later)
                    print()
                    something_rearranged = True
    return something_rearranged

def assigngamestodates(allseriesdates):
    seasonlength=0
    for d in allseriesdates:
        seasonlength=seasonlength+d.length
    print('Season is '+str(seasonlength)+' days long.')
    openingday=allseriesdates[0].startdate
    print('Opening day is '+str(openingday))
    print('Last day of season is '+str(openingday+timedelta(seasonlength-1)))
    gamedays = [ [] for d in range(0,seasonlength) ]
    for d in allseriesdates:
        day = d.startdate
        i = (day - openingday).days
        for s in d.serieslist:
            for m in matchups[s.seriestype][s.seriesnum]:
                if s.reversed:
                    hometeam = teams[s.awaydiv][m[1]]
                    awayteam = teams[s.homediv][m[0]]
                else:
                    hometeam = teams[s.homediv][m[0]]
                    awayteam = teams[s.awaydiv][m[1]]
                if d.length-s.numgames == 2:
                    first = 1
                    last = d.length-1
                elif random.randint(0,1) and not d.datetype == 'weekend':
                    first = 0
                    last = s.numgames
                else:
                    first = d.length-s.numgames
                    last = d.length
                for j in range(first,last):
                    gamedays[i+j].append((hometeam, awayteam))
    for d in range(0,seasonlength):
        print(str(openingday+timedelta(d))+': '+str(gamedays[d]))
    return gamedays
                
def check_for_consecutive_series(allseriesdates):
    x = dict()
    prev = None
    for d in allseriesdates:
        day = str(d.startdate)
        x[day] = []
        for s in d.serieslist:
            for m in matchups[s.seriestype][s.seriesnum]:
                hometeam = teams[s.homediv][m[0]]
                awayteam = teams[s.awaydiv][m[1]]
                x[day].append(sorted([hometeam, awayteam]))
        if prev != None:
            for i in x[day]:
                for j in prev:
                    if i == j:
                        print("ERROR!!!   "+str(i))
                        print(day)
                        print(d)
                        print(x[day])
                        return False

        prev=x[day]
    return True

def check_series_length(allseriesdates):
    found_issue = False
    for d in allseriesdates:
        for s in d.serieslist:
            if d.length < s.numgames:
                print('Error:  too many games in too few days')
                print(d)
                print(s)
                found_issue = True
    return found_issue

def check_for_offdays(schedule):
    allteams = [ team for div in teams for team in teams[div]]
    for thisteam in allteams:
        streak = 0
        for d in range(0,len(schedule)):
            teams_playing_today = [ team for game in schedule[d] for team in game]
            if thisteam in teams_playing_today:
                streak=streak+1
            else:
                if streak == 0:
                    firstdate=openingday(year)+timedelta(d-1)
                    firststr=firstdate.strftime('%a')+' '+str(firstdate)
                    lastdate=openingday(year)+timedelta(d)
                    laststr=lastdate.strftime('%a')+' '+str(lastdate)
                    print(thisteam+' has two consecutive days off: '+firststr+' and '+laststr)
                if streak > 20:
                    firstdate=openingday(year)+timedelta(d-streak)
                    firststr=firstdate.strftime('%a')+' '+str(firstdate)
                    lastdate=openingday(year)+timedelta(d-1)
                    laststr=lastdate.strftime('%a')+' '+str(lastdate)
                    print(thisteam+' plays '+str(streak)+' consecutive games starting '+firststr+' and ending '+laststr)
                streak=0
                #print(thisteam+' has an off day on '+str(openingday(year)+timedelta(d)))

def create_schedule(allseriesdates,allseries):
    assignholidayseries(allseriesdates,allseries)
    assignfourgamedivdiv(allseriesdates,allseries)
    assignthreegamedivdiv(allseriesdates,allseries)
    assignfourgameroundrobin(allseriesdates,allseries)
    assignthreegameweekendroundrobin(allseriesdates,allseries)
    try:
        assignthreegameweekdayroundrobin(allseriesdates,allseries)
    except:
        for s in allseriesdates:
            print(str(s.startdate)+':('+str(s.length)+'):'+str(s.serieslist))
        print(allseries)

    assignthreegameweekdayroundrobin(allseriesdates,allseries)
    if (len(allseries)):
        print(str(len(series))+' series were not assigned.')
        return False

    print()
    if check_series_length(allseriesdates):
        print(allseriesdates)
        return False
        
    numiters=1
    while rearrange_series(allseriesdates):
        numiters=numiters+1
        continue
    print('Resolved in '+str(numiters)+' iterations.')
    if not check_for_consecutive_series(allseriesdates):
        print(allseriesdates)
        return False

    for s in allseriesdates:
        print(str(s.startdate)+':('+str(s.length)+'):'+str(s.serieslist))

    print()
    print()
    if check_series_length(allseriesdates):
        print(allseriesdates)
        return False

    schedule = assigngamestodates(allseriesdates)

    check_for_offdays(schedule)
    return True

allseriesdates = initializeseriesdates()
matchups = initializematchups()
allseries = initializeseries()
if not create_schedule(allseriesdates,allseries):
    print('Schedule creation failed.  See above messages for details.')

