from collections import namedtuple
from datetime import date
from datetime import timedelta
from collections import namedtuple
import calendar
import random
import csv

year=1961
mlbdivisions = ['American', 'National', 'Western']
teams = { 'American' : ['NYY', 'BAL', 'BOS', 'CLE', 'WAS', 'DET'],
          'National' : ['BKN', 'PIT', 'MIL', 'CIN', 'PHI', 'CHI'],
          'Western' : ['STL', 'COL', 'DAL', 'LA', 'KC', 'SF'],
        }
maxdayswithoutoffday = 21
maxhomestand = 15
maxroadtrip = 14

seriesdates = namedtuple('seriesdates', 'startdate, length, datetype, serieslist')
series = namedtuple('series', 'seriestype homediv awaydiv numgames seriesnum reversed')
matchup = namedtuple('matchup', 'home away')
gameday = namedtuple('date', 'gamelist')
game = namedtuple('home', 'away')
homeawayswap = namedtuple('homeawayswap','matchup swaplist movelist')
swapdate = namedtuple('swapdate', 'fromdate todate')

def openingday(y=year):
    startdate=date(y,4,7)
    startdate=startdate+timedelta(4-startdate.weekday())
    return startdate

def format_date(d):
    thisdate=openingday(year)+timedelta(d)
    datestr=thisdate.strftime('%a')+' '+str(thisdate)
    return datestr

def get_day_of_week(d):
    thisdate=openingday(year)+timedelta(d)
    return thisdate.strftime('%a')
    
def isaholiday(d):

    mydate = openingday()+timedelta(d)
    memorialday=calendar.Calendar().monthdatescalendar(year,5)[-1][0]
    fourthofjuly=date(year,7,4)
    laborday=calendar.Calendar().monthdatescalendar(year,9)[1][0]

    if mydate == memorialday:
        return 1
    elif mydate == fourthofjuly:
        return 1
    elif mydate == laborday:
        return 1
    elif mydate == openingday():
        return 1
    else:
        return 0

def initializeseriesdates():

    dates=[]
    d=0
    dates.append(seriesdates(d,3,'holiday',[]))
    d=3

    for w in range(0,24):
        if get_day_of_week(d) == 'Tue':
            dates.append(seriesdates(d,3,'weekday',[]))
            d=d+3
            dates.append(seriesdates(d,3,'weekend',[]))
            d=d+3
        elif isaholiday(d+7):
            dates.append(seriesdates(d,4,'weekday',[]))
            d=d+4
            dates.append(seriesdates(d,4,'holiday',[]))
            d=d+4
        else:
            dates.append(seriesdates(d,3,'weekday',[]))
            d=d+3
            dates.append(seriesdates(d,4,'weekend',[]))
            d=d+4
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

# To spread out the days off, we try to avoid scheduling a divdiv series
# for the same division three times in a row.
def search_for_blackout_div(dates,current_date):
    blackoutdiv = 'NoBlackout'
    divisions_playing = set()
    if current_date > 2:
        d = dates[current_date-1]
        for s in d.serieslist:
            if s.seriestype == 'divdiv':
                divisions_playing.add(s.homediv)
                divisions_playing.add(s.awaydiv)
        d = dates[current_date-2]
        for s in d.serieslist:
            if s.seriestype == 'divdiv':
                if s.homediv in divisions_playing:
                    return s.homediv
                elif s.awaydiv in divisions_playing:
                    return s.awaydiv
    return 'NoBlackout'

def assigndivdiv(dates,series):
    for r in range(0,len(dates)):
        d = dates[r]
        if d.serieslist != []:
            continue
        if d.length == 4 and d.datetype == 'weekend':
            blackout = search_for_blackout_div(dates,r)
            #print('Blackout division for '+str(d)+' is '+blackout)
            try:
                divdivseries = popdivdivseries(series,4,blackout)
            except:
                try:
                    divdivseries = popdivdivseries(series,4)
                except:
                    return None
            d.serieslist.append(divdivseries)
            divlist = mlbdivisions.copy()
            divlist.remove(divdivseries.homediv)
            divlist.remove(divdivseries.awaydiv)
            d.serieslist.append(poproundrobinseriesexact(series,divlist[0],3))
        elif d.length == 3 and get_day_of_week(d.startdate) == 'Mon':
            blackout = search_for_blackout_div(dates,r)
            #print('Blackout division for '+str(d)+' is '+blackout)
            try:
                divdivseries = popdivdivseries(series,3,blackout)
            except:
                #print('Unable to find a series not containing the '+blackout+' division on '+str(d))
                continue
            #print('Assigning :'+str(divdivseries))
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
        if not len(series):
            break

def assignfourgameroundrobin(dates,series):
    for d in reversed(dates):
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
        if abs(seriesdate.startdate-replacementdate.startdate) < 10:
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
                print("replacement series: "+format_date(seriesdate.startdate)+':'+str(replacementseries))
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
                    print('Two consecutive series between same sets of teams:'+format_date(earlier.startdate)+':'+format_date(later.startdate))
                    print(earlier)
                    print(later)
                    # Can't easily swap holiday series, so choose the non-holiday one
                    if earlier.datetype == 'holiday':
                        swap_series(allseriesdates,later,j)
                    else:
                        swap_series(allseriesdates,earlier,i)
                    print('After replacement')
                    print(earlier)
                    print(later)
                    print()
                    something_rearranged = True
    return something_rearranged

def print_schedule(schedule):
    print()
    print('----Begin schedule----')
    for d in range(0,len(schedule)):
        print(format_date(d)+': '+str(schedule[d]))
    print('-----End schedule-----')
    print()

def print_series_dates(dates):
    for s in dates:
        print(format_date(s.startdate)+':('+str(s.length)+'):'+str(s.serieslist))

        
def assigngamestodates(allseriesdates):
    seasonlength=0
    for d in allseriesdates:
        seasonlength=seasonlength+d.length
    print('Season is '+str(seasonlength)+' days long.')
    openingday=allseriesdates[0].startdate
    print('Opening day is '+format_date(openingday))
    print('Last day of season is '+format_date(openingday+seasonlength-1))
    gamedays = [ [] for d in range(0,seasonlength) ]
    for d in allseriesdates:
        i = d.startdate
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
    #print_schedule(gamedays)
    return gamedays
                
def check_for_consecutive_series(allseriesdates):
    x = dict()
    prev = None
    for d in allseriesdates:
        day = d.startdate
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
    all_okay = True
    allteams = [ team for div in teams for team in teams[div]]
    for thisteam in allteams:
        streak = 0
        prevstreak=0
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
                    all_okay = False
                if streak > maxdayswithoutoffday:
                    firstdate=openingday(year)+timedelta(d-streak)
                    firststr=firstdate.strftime('%a')+' '+str(firstdate)
                    lastdate=openingday(year)+timedelta(d-1)
                    laststr=lastdate.strftime('%a')+' '+str(lastdate)
                    print(thisteam+' plays '+str(streak)+' consecutive games starting '+firststr+' and ending '+laststr)
                    all_okay = False
                prevstreak=streak
                streak=0
    return all_okay

def check_for_long_homestands_and_roadtrips(schedule):
    all_okay =  True
    allteams = [ team for div in teams for team in teams[div]]
    for thisteam in allteams:
        homestand=0
        roadtrip=0
        for d in range(0,len(schedule)):
            home_teams = [ game[0] for game in schedule[d]]
            away_teams = [ game[1] for game in schedule[d]]
            if thisteam in home_teams:
                if roadtrip > maxroadtrip:
                    print(thisteam+' has a '+str(roadtrip)+' game road trip ending on '+format_date(d))
                    all_okay = False
                roadtrip = 0
                homestand = homestand+1
            elif thisteam in away_teams:
                if homestand > maxhomestand:
                    print(thisteam+' has a '+str(homestand)+' game homestand ending on '+format_date(d))
                    all_okay = False
                homestand=0
                roadtrip = roadtrip +1
        if roadtrip > maxroadtrip:
            print(thisteam+' ends season with a '+str(roadtrip)+' game road trip.')
            all_okay = False
        elif homestand > maxhomestand:
            print(thisteam+' ends season with a '+str(homestand)+' game home stand.')
            all_okay = False
    return all_okay

def find_home_away_swap(schedule,matchup,series_start_date,series_length,fixupdays):
    fixlist = []
    d = 0
    possible4to2swap = None
    while d < len(schedule):
        matchup_length = 0
        while d < len(schedule) and schedule_contains_matchup(schedule,d,matchup[1],matchup[0]):
            d=d+1
            matchup_length=matchup_length+1
        if matchup_length > 0:
            if (matchup_length == series_length):
                #print('Found series to home/away swap with from '+format_date(d-matchup_length)+' to '+format_date(d-1))
                swap = homeawayswap(matchup,[],[])
                for i in range(0,series_length):
                    swap.swaplist.append((series_start_date+i, d-matchup_length+i)) 
                fixlist.append(swap)
            elif matchup_length == 4 and series_length == 3:
                #print('Possible series to home/away swap with from '+format_date(d-matchup_length)+' to '+format_date(d-1))
                date_before = series_start_date-1
                if (matchup[0] in fixupdays[date_before] and
                    matchup[1] in fixupdays[date_before] and
                    get_day_of_week(date_before) in ['Mon', 'Thu'] and
                    get_day_of_week(d-matchup_length) in ['Mon', 'Thu']):
                    print('Can swap(before) '+str(matchup_length)+' days from '+format_date(date_before)+' until '+format_date(date_before+matchup_length-1))
                    print('    with '+format_date(d-matchup_length)+' until '+format_date(d-1))
                    swap = homeawayswap((matchup[1], matchup[0]),[],[])
                    for i in range(0,series_length):
                        swap.swaplist.append((d-matchup_length+1+i, series_start_date+i))
                    swap.movelist.append((d-matchup_length,date_before))
                    fixlist.append(swap)
                date_after = series_start_date+series_length
                if (matchup[0] in fixupdays[date_after] and
                    matchup[1] in fixupdays[date_after] and
                    get_day_of_week(date_after) in ['Thu', 'Mon'] and
                    get_day_of_week(d-matchup_length) in ['Mon', 'Thu']):
                    print('Can swap(after) '+str(matchup_length)+' days from '+format_date(series_start_date)+' until '+format_date(date_after))
                    print('    with '+format_date(d-matchup_length)+' until '+format_date(d-1))
                    swap = homeawayswap((matchup[1], matchup[0]),[],[])
                    for i in range(0,series_length):
                        swap.swaplist.append((d-series_length+i, series_start_date+i))
                    swap.movelist.append((d-matchup_length,series_start_date+matchup_length-1))
                    fixlist.append(swap)
            elif series_length == 4 and matchup_length == 2:
                if possible4to2swap == None:
                    #print('Found first 2 game series to possibly home/away swap with from '+format_date(d-matchup_length)+' to '+format_date(d-1))
                    possible4to2swap = homeawayswap(matchup,[],[])
                    for i in range(0,matchup_length):
                        possible4to2swap.swaplist.append((series_start_date+i, d-matchup_length+i))
                else:
                    #print('Found second 2 game series to home/away swap with from '+format_date(d-matchup_length)+' to '+format_date(d-1))
                    for i in range(2,series_length):
                        possible4to2swap.swaplist.append((series_start_date+i, d-series_length+i))
                    fixlist.append(possible4to2swap)
                    possible4to2swap = None
        d = d+1
    return fixlist

def fix_long_streak(schedule,team,firstgame,lastgame,fixupdays):
    firstdate=lastgame-maxhomestand
    lastdate=firstgame+maxhomestand
    swaps = list()
    while(get_matchup_for_team(schedule,firstdate,team) == get_matchup_for_team(schedule,firstdate-1,team)):
        firstdate = firstdate-1
    while(get_matchup_for_team(schedule,lastdate,team) == get_matchup_for_team(schedule,lastdate+1,team)):
        lastdate = lastdate+1
    print(team+':  Need to home/away swap a series between '+format_date(firstdate) +' and '+format_date(lastdate))
    d=firstdate
    while d <= lastdate:
        m = get_matchup_for_team(schedule,d,team)
        if m != None:
            start = d
            nextm = get_matchup_for_team(schedule,d+1,team)
            while m == nextm:
                d=d+1
                nextm = get_matchup_for_team(schedule,d+1,team)
            #print(str(d-start+1)+' game series between '+str(m)+' from '+format_date(start)+' to '+format_date(d))
            swaps = swaps + find_home_away_swap(schedule,m,start,d-start+1,fixupdays)
        d=d+1
    if len(swaps):
        chosenswap = random.choice(swaps)
        print(chosenswap)
        print('Swapping '+str(chosenswap.matchup))
        #print('... '+str(chosenswap.length)+' games from '+format_date(chosenswap.fromdate)+' to '+format_date(chosenswap.todate))
        #print('... '+str(chosenswap.revlength)+' games from '+format_date(chosenswap.revfromdate)+' to '+format_date(chosenswap.revtodate))
        reversedmatchup = ( chosenswap.matchup[1], chosenswap.matchup[0] )
        for i in range(0,len(chosenswap.swaplist)):
            print('Swapping '+format_date(chosenswap.swaplist[i][0])+' and '+format_date(chosenswap.swaplist[i][1]))
            schedule[chosenswap.swaplist[i][0]].remove(chosenswap.matchup)
            schedule[chosenswap.swaplist[i][1]].append(chosenswap.matchup)
            schedule[chosenswap.swaplist[i][1]].remove(reversedmatchup)
            schedule[chosenswap.swaplist[i][0]].append(reversedmatchup)
        for i in range(0,len(chosenswap.movelist)):
            print('Moving '+format_date(chosenswap.movelist[i][0])+' to '+format_date(chosenswap.movelist[i][1]))
            schedule[chosenswap.movelist[i][0]].remove(chosenswap.matchup)
            schedule[chosenswap.movelist[i][1]].append(chosenswap.matchup)
        return True
    return False
                
def fix_long_homestands(schedule,fixupdays):
    allteams = [ team for div in teams for team in teams[div]]
    random.shuffle(allteams)
    for thisteam in allteams:
        homestand=0
        for d in range(0,len(schedule)):
            home_teams = [ game[0] for game in schedule[d]]
            away_teams = [ game[1] for game in schedule[d]]
            if thisteam in home_teams:
                if (homestand == 0):
                    firstgameofhomestand=d
                homestand = homestand+1
                lasthomegame = d
            elif thisteam in away_teams:
                if homestand > maxhomestand:
                    print(thisteam+' has a '+str(homestand)+' game homestand starting on '+
                          format_date(firstgameofhomestand)+' and ending on '+format_date(lasthomegame))
                    if fix_long_streak(schedule,thisteam,firstgameofhomestand,lasthomegame,fixupdays):
                        return True
                homestand=0
        if homestand > maxhomestand:
            print(thisteam+' has a '+str(homestand)+' game homestand starting on '+
                format_date(firstgameofhomestand)+' and ending on '+format_date(lasthomegame))
            if fix_long_streak(schedule,thisteam,firstgameofhomestand,lasthomegame,fixupdays):
                return True
    return False

def fix_long_roadtrips(schedule,fixupdays):
    allteams = [ team for div in teams for team in teams[div]]
    random.shuffle(allteams)
    for thisteam in allteams:
        roadtriplen=0
        for d in range(0,len(schedule)):
            home_teams = [ game[0] for game in schedule[d]]
            away_teams = [ game[1] for game in schedule[d]]
            if thisteam in away_teams:
                if (roadtriplen == 0):
                    firstgameofroadtrip=d
                roadtriplen = roadtriplen+1
                lastgameoftrip = d
            elif thisteam in home_teams:
                if roadtriplen > maxroadtrip:
                    print(thisteam+' has a '+str(roadtriplen)+' game road trip starting on '+
                          format_date(firstgameofroadtrip)+' and ending on '+format_date(lastgameoftrip))
                    if fix_long_streak(schedule,thisteam,firstgameofroadtrip,lastgameoftrip,fixupdays):
                        return True
                roadtriplen=0
        if roadtriplen > maxroadtrip:
            print(thisteam+' has a '+str(roadtriplen)+' game road trip starting on '+
                    format_date(firstgameofroadtrip)+' and ending on '+format_date(lastgameoftrip))
            if fix_long_streak(schedule,thisteam,firstgameofroadtrip,lastgameoftrip,fixupdays):
                return True
    return False
                
def check_schedule(schedule):
    all_okay = check_for_offdays(schedule) and check_for_long_homestands_and_roadtrips(schedule)
    for d in range(0,len(schedule)):
        if schedule[d] == []:
            print('No games scheduled for '+format_date(d))
            all_okay = False
        allteamsplayingtoday = [ team for game in schedule[d] for team in game]        
        if len(allteamsplayingtoday) < 18:
            if get_day_of_week(d) in ['Fri', 'Sat', 'Sun']:
                print('Some teams are not scheduled to play on '+format_date(d))
                all_okay=False
            elif isaholiday(d):
                print('Some teams are not scheduled to play on '+format_date(d)+ 'which is a holiday.')
                all_okay=False
        setofteamsplayingtoday = set(allteamsplayingtoday)       
        if (len(allteamsplayingtoday) != len(setofteamsplayingtoday)):
            print('Issue with teams playing on '+format_date(d))
            print(allteamsplayingtoday)
            all_okay = False
    if get_matchup_for_team(schedule,0,'CIN')[0] != 'CIN':
        print('CIN not home on opening day')
        all_okay = False
            
    return all_okay

def create_offday_fixup_list(schedule):
    teamsavailabletoplayonthisoffday = [ set() for d in range(0,len(schedule)) ]
    allteams = [ team for div in teams for team in teams[div]]
    for thisteam in allteams:
        streak = 0
        prevstreak = 0
        for d in range(0,len(schedule)):
            teams_playing_today = [ team for game in schedule[d] for team in game]
            if thisteam in teams_playing_today:
                streak=streak+1
            else:
                if prevstreak > 0 and prevstreak+streak < maxdayswithoutoffday:
                    teamsavailabletoplayonthisoffday[prev].add(thisteam)
                prev = d
                prevstreak = streak
                streak = 0
        if prevstreak > 0 and prevstreak+streak < maxdayswithoutoffday:
            teamsavailabletoplayonthisoffday[prev].add(thisteam)
    for d in range(0,len(teamsavailabletoplayonthisoffday)):
        if len(teamsavailabletoplayonthisoffday[d]):
            offday=openingday(year)+timedelta(d)
            offdaystr=offday.strftime('%a')+' '+str(offday)
            #print('The following teams can have a game added to current off day '+format_date(d)+':') 
            #print('.... '+str(teamsavailabletoplayonthisoffday[d]))
    return teamsavailabletoplayonthisoffday

def schedule_contains_matchup(schedule,d,team1,team2):
    for g in schedule[d]:
        if g[0] == team1 and g[1] == team2:
            return True
    return False

def find_open_day_to_move_game_to(schedule,date_to_free_up,matchup,fixupdays):
    newdatelist = []
    for d in range(0,len(fixupdays)):
        if matchup[0] in fixupdays[d] and matchup[1] in fixupdays[d]:
            print(matchup[0]+' and '+matchup[1]+' both are available on '+format_date(d))
            if (schedule_contains_matchup(schedule,d-1,matchup[0],matchup[1]) or
                schedule_contains_matchup(schedule,d+1,matchup[0],matchup[1]) ):
                print('Can move game between '+matchup[0]+' and '+matchup[1]+' from '+
                      format_date(date_to_free_up)+' to '+format_date(d))
                newdatelist.append(d)
    if len(newdatelist):
        date_to_move_to = random.choice(newdatelist)
        schedule[date_to_free_up].remove(matchup)
        schedule[date_to_move_to].append(matchup)
        print('Moving game between '+matchup[0]+' and '+matchup[1]+' from '+
                      format_date(date_to_free_up)+' to '+format_date(date_to_move_to))
        return True
    else:
        return False

def find_and_make_series_swap(schedule,date_to_free_up,matchup,fixupdays):
    print('=====find_and_make_series_swap=====')
    for d in range(0,len(schedule)):
        if matchup[0] in fixupdays[d] and matchup[1] in fixupdays[d]:
            print(matchup[0]+' and '+matchup[1]+' both are available on '+format_date(d))
            if schedule_contains_matchup(schedule,d+1,matchup[1],matchup[0]):
                to_series_count=1
                while schedule_contains_matchup(schedule,d+1+to_series_count,matchup[1],matchup[0]):
                    to_series_count=to_series_count+1
                print('..and they play in a '+str(to_series_count)+' game series in other stadium on '+format_date(d+to_series_count))
                if schedule_contains_matchup(schedule,date_to_free_up+1,matchup[0],matchup[1]):
                    from_series_count=2
                    while schedule_contains_matchup(schedule,date_to_free_up+from_series_count,matchup[0],matchup[1]):
                        from_series_count=from_series_count+1
                    if (from_series_count == to_series_count+1):
                        print('....to be swapped with a '+str(from_series_count)+' game series starting on '+format_date(date_to_free_up))
                        for i in range(0,from_series_count):
                            schedule[date_to_free_up+i].remove(matchup)
                            schedule[d+i].append(matchup)
                        reverse_matchup = matchup[1], matchup[0]
                        for i in range(1,from_series_count):
                            schedule[d+i].remove(reverse_matchup)
                            schedule[date_to_free_up+i].append(reverse_matchup)
                        return True
                elif schedule_contains_matchup(schedule,date_to_free_up-1,matchup[0],matchup[1]):
                    from_series_count=2
                    while schedule_contains_matchup(schedule,date_to_free_up-from_series_count,matchup[0],matchup[1]):
                        from_series_count=from_series_count+1
                    if (from_series_count == to_series_count+1):
                        print('....to be swapped with a '+str(from_series_count)+' game series ending on '+format_date(date_to_free_up))
                        for i in range(0,from_series_count):
                            schedule[date_to_free_up-i].remove(matchup)
                            schedule[d+i].append(matchup)
                        reverse_matchup = matchup[1], matchup[0]
                        for i in range(1,from_series_count):
                            schedule[d+i].remove(reverse_matchup)
                            schedule[date_to_free_up-i].append(reverse_matchup)
                        return True
    return False

def shift_two_game_series_to_make_room(schedule,date_to_free_up,matchup,fixupdays):
    print('=====shift_two_game_series_to_make_room=====')
    for d in range(0,len(schedule)):
        if matchup[0] in fixupdays[d] and matchup[1] in fixupdays[d]:
            print(matchup[0]+' and '+matchup[1]+' both are available on '+format_date(d))
            if schedule_contains_matchup(schedule,d+3,matchup[0],matchup[1]):
                other_match_home = get_matchup_for_team(schedule,d+1,matchup[0])
                other_team1 = [ team for team in other_match_home if team != matchup[0]][0]
                other_match_away = get_matchup_for_team(schedule,d+1,matchup[1])
                other_team2 = [ team for team in other_match_away if team != matchup[1]][0]
                if (get_matchup_for_team(schedule,d+2,matchup[0]) == other_match_home and
                    get_matchup_for_team(schedule,d+2,matchup[1]) == other_match_away and
                    get_matchup_for_team(schedule,d,matchup[0]) == None and
                    get_matchup_for_team(schedule,d,matchup[1]) == None):
                    print('Shifting games from '+format_date(d+2)+' to '+format_date(d))
                    print('  to allow moving of '+str(matchup)+' from ' +format_date(date_to_free_up)+' to '+format_date(d+2))
                    schedule[d].append(other_match_home)
                    schedule[d+2].remove(other_match_home)
                    schedule[d].append(other_match_away)
                    schedule[d+2].remove(other_match_away)
                    schedule[d+2].append(matchup)
                    schedule[date_to_free_up].remove(matchup)
                    return True
    return False

def get_matchup_for_team(schedule,d,thisteam):
    if d >= len(schedule):
        return None
    for t in schedule[d]:
        if t[0] == thisteam or t[1] == thisteam:
            return t
    return None
    
def find_and_fix_long_streak(schedule,fixupdays):
    print('-----')
    allteams = [ team for div in teams for team in teams[div]]
    for thisteam in allteams:
        streak = 0
        prevstreak=0
        for d in range(0,len(schedule)):
            teams_playing_today = [ team for game in schedule[d] for team in game]
            if thisteam in teams_playing_today:
                streak=streak+1
            else:
                if streak > maxdayswithoutoffday:
                    firstd = max(d-maxdayswithoutoffday-1,d-streak+3)
                    lastd = min(d-streak+maxdayswithoutoffday+1,d-3)
                    print(thisteam+' plays '+str(streak)+' consecutive games starting '+format_date(d-streak)+' and ending '+format_date(d-1))
                    print('Need to create an open date between '+format_date(firstd)+' and '+format_date(lastd-1))
                    for i in range(firstd,lastd):
                        dayofweek=get_day_of_week(i)
                        if dayofweek in ['Mon', 'Wed', 'Thu']:
                            if isaholiday(i):
                                print(format_date(i)+' is a holiday')
                                continue
                            m = get_matchup_for_team(schedule,i,thisteam)
                            print('Search for a swap date for '+str(m)+' on '+format_date(i))
                            if find_open_day_to_move_game_to(schedule,i,m,fixupdays):
                                return True
                            if find_and_make_series_swap(schedule,i,m,fixupdays):
                                return True
                            if shift_two_game_series_to_make_room(schedule,i,m,fixupdays):
                                return True
                    print('Unable to create an open date between '+format_date(firstd)+' and '+format_date(lastd-1))
                    return False
                prevstreak=streak
                streak=0
    return False

def ensure_CIN_starts_at_home(schedule,fixupdays):
    m = get_matchup_for_team(schedule,0,'CIN')
    if m[0] != 'CIN':
        print('Swapping opening series for CIN to ensure they start at home')
        swaps = find_home_away_swap(schedule,m,0,3,fixupdays)
        if len(swaps) != 1:
            raise
        swap = swaps[0]
        if len(swap.swaplist) != 3 or len(swap.movelist) != 0:
            raise
        print('Swapping '+str(swap.matchup))
        reversedmatchup = ( swap.matchup[1], swap.matchup[0] )
        for i in range(0,len(swap.swaplist)):
            print('Swapping '+format_date(swap.swaplist[i][0])+' and '+format_date(swap.swaplist[i][1]))
            schedule[swap.swaplist[i][0]].remove(swap.matchup)
            schedule[swap.swaplist[i][1]].append(swap.matchup)
            schedule[swap.swaplist[i][1]].remove(reversedmatchup)
            schedule[swap.swaplist[i][0]].append(reversedmatchup)

def fill_open_dates(schedule,fixupdays):
    for d in range(0,len(schedule)):
        if schedule[d] == []:
            allteams = fixupdays[d].copy()
            thisteam = random.sample(allteams,1)[0]
            allteams.remove(thisteam)
            if get_day_of_week(d) == 'Mon':
                m = get_matchup_for_team(schedule,d+1,thisteam)
                otherteam = [t for t in m if t != thisteam][0]
                if (otherteam in allteams and
                    get_matchup_for_team(schedule,d+2,thisteam) == m ):
                    if (get_matchup_for_team(schedule,d+3,thisteam) != m and
                        get_matchup_for_team(schedule,d+3,thisteam) != None and
                        get_matchup_for_team(schedule,d+3,otherteam) != None):
                        print('Moving '+str(m)+' on '+format_date(d+2)+' to '+format_date(d))
                        schedule[d].append(m)
                        schedule[d+2].remove(m)
                        continue
                    elif (get_matchup_for_team(schedule,d+3,thisteam) == m and
                        get_matchup_for_team(schedule,d+4,thisteam) != None and
                        get_matchup_for_team(schedule,d+4,otherteam) != None):
                        print('Moving '+str(m)+' on '+format_date(d+3)+' to '+format_date(d))
                        schedule[d].append(m)
                        schedule[d+3].remove(m)
                        continue
                m = get_matchup_for_team(schedule,d-1,thisteam)
                otherteam = [t for t in m if t != thisteam][0]
                if (otherteam in allteams and
                    get_matchup_for_team(schedule,d-2,thisteam) == m and
                    get_matchup_for_team(schedule,d-3,thisteam) == m and
                    get_matchup_for_team(schedule,d-4,thisteam) == m and
                    get_matchup_for_team(schedule,d-5,thisteam) != None and
                    get_matchup_for_team(schedule,d-5,otherteam) != None):
                    print('Moving '+str(m)+' on '+format_date(d-4)+' to '+format_date(d))
                    schedule[d].append(m)
                    schedule[d-4].remove(m)
                    continue
                print('Unable to find a way to fill open day on '+format_date(d))
                return False
            else:
                print('Need logic to implement fill_open_dates on '+get_day_of_week(d))
                raise                
    return True
                
                
def fix_consecutive_offdays(schedule):
    allteams = [ team for div in teams for team in teams[div]]
    for thisteam in allteams:
        for d in range(0,len(schedule)-1):
            teams_playing_today = [ team for game in schedule[d] for team in game]
            teams_playing_tomorrow = [ team for game in schedule[d+1] for team in game]
            if thisteam not in teams_playing_today and thisteam not in teams_playing_tomorrow:
                firstdate=openingday(year)+timedelta(d)
                firststr=firstdate.strftime('%a')+' '+str(firstdate)
                lastdate=openingday(year)+timedelta(d+1)
                laststr=lastdate.strftime('%a')+' '+str(lastdate)
                print(thisteam+' has two consecutive days off: '+firststr+' and '+laststr)
                dayofweek = (openingday(year)+timedelta(d)).strftime('%a')
                if (dayofweek == 'Wed'):
                    for gMon in schedule[d-2]:
                        if gMon[0] == thisteam:
                            otherteam = gMon[1]
                        elif gMon[1] == thisteam:
                            otherteam = gMon[0]
                        else:
                            continue
                        if otherteam not in teams_playing_today:
                            found_Tue_game = False
                            for gTue in schedule[d-1]:
                                if (gTue[0] in [thisteam,otherteam] and
                                    gTue[1] in [thisteam,otherteam] and
                                    gMon[0] == gTue[0]):
                                    found_Tue_game = True
                                    break
                            today = str(openingday(year)+timedelta(d))
                            twodaysago = str(openingday(year)+timedelta(d-2))
                            print('Moving game between '+thisteam+' and '+otherteam+' from '+twodaysago+' to '+today)
                            schedule[d-2].remove(gMon)
                            schedule[d].append(gMon)
                            if not found_Tue_game:
                                print('Did not find Tuesday game between these teams')
                                raise
                        break
                else:
                    print('Fixing offday issues on days other than Wed not yet supported')
                    raise
    return

def compute_game_time(schedule,d,hometeam,awayteam,teamdata):

    if get_day_of_week(d) in ['Sat', 'Sun'] or isaholiday(d):
        gametime = int(teamdata[hometeam]['day_start'])
    else:
        gametime = int(teamdata[hometeam]['night_start'])
    max_distance_to_travel = 0
    hometeamtomorrow = get_matchup_for_team(schedule,d+1,hometeam)
    if hometeamtomorrow != None:
        dist_to_travel=int(teamdata[hometeam][hometeamtomorrow[0]])
        max_distance_to_travel=max(max_distance_to_travel,dist_to_travel)
    awayteamtomorrow = get_matchup_for_team(schedule,d+1,awayteam)
    if awayteamtomorrow != None:
        dist_to_travel=int(teamdata[hometeam][awayteamtomorrow[0]])
        max_distance_to_travel=max(max_distance_to_travel,dist_to_travel)
    if max_distance_to_travel > 1000:
        gametime = min(gametime,int(teamdata[hometeam]['getaway_start']))
    gametime = gametime + int(teamdata[hometeam]['timezone'])*100
    return gametime
    

def write_schedule(schedule):
    teamdata = {}
    with open('/Users/Dad/ootpsched/ootpsched.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            teamdata[row['team']] = row
    type='ILN_BGN_G154_SL1_D3_T6_T6_T6_C_'+str(year)
    outfilename='c:/Users/Dad/OOTPschedules/'+type+'.lsdl'
    f=open(outfilename,'w')
    print('<?xml version="1.0" encoding="ISO-8859-1"?>',file=f)
    print('<SCHEDULE type="ILN_BGN_G154_SL1D3T6T6T6" inter_league="0" balanced_games="0" games_per_team="154" start_day_of_week="6">',file=f)
    print('<GAMES>',file=f)
    for d in range(0,len(schedule)):
        for m in schedule[d]:
            hometeam=m[0]
            awayteam=m[1]
            time=compute_game_time(schedule,d,hometeam,awayteam,teamdata)
            hometeamnum=str(teamdata[hometeam]['teamnum'])
            awayteamnum=str(teamdata[awayteam]['teamnum'])
            print('<GAME day="'+str(d+1)+'" time="'+str(time)+'" away="'+awayteamnum+'" home="'+hometeamnum+'" />',file=f)
    print('</GAMES>',file=f)
    print('</SCHEDULE>',file=f)
    f.close()

def create_schedule(allseriesdates,allseries):
    assignholidayseries(allseriesdates,allseries)
    assigndivdiv(allseriesdates,allseries)
    assignfourgameroundrobin(allseriesdates,allseries)
    assignthreegameweekendroundrobin(allseriesdates,allseries)
    try:
        assignthreegameweekdayroundrobin(allseriesdates,allseries)
    except:
        print_series_dates(allseriesdates)
        print(allseries)
    if (len(allseries)):
        print(str(len(series))+' series were not assigned.')
        return False

    if check_series_length(allseriesdates):
        print_series_dates(allseriesdates)
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
        print(format_date(s.startdate)+':('+str(s.length)+'):'+str(s.serieslist))

    if check_series_length(allseriesdates):
        print_series_dates(allseriesdates)
        return False

    schedule = assigngamestodates(allseriesdates)
    
    offdayfixuplist = create_offday_fixup_list(schedule)
    ensure_CIN_starts_at_home(schedule,offdayfixuplist)
    
    iters=0
    while iters < 200:
        iters=iters+1
        try:
            fix_consecutive_offdays(schedule)
        except:
            print('Failure during fix_consecutive_offdays')
            return False
        offdayfixuplist = create_offday_fixup_list(schedule)
        fill_open_dates(schedule,offdayfixuplist)
        offdayfixuplist = create_offday_fixup_list(schedule)
        if find_and_fix_long_streak(schedule,offdayfixuplist):
            continue
        offdayfixuplist = create_offday_fixup_list(schedule)
        if fix_long_homestands(schedule,offdayfixuplist):
            continue
        if not fix_long_roadtrips(schedule,offdayfixuplist):
            break
    if not check_schedule(schedule):
        return False
    print_schedule(schedule)
    write_schedule(schedule)
    return True      

random.seed(2)
iters=0
while iters < 10:
    allseriesdates = initializeseriesdates()
    matchups = initializematchups()
    allseries = initializeseries()
    if not create_schedule(allseriesdates,allseries):
        print('Schedule creation failed.  See above messages for details.  Will try to generate another schedule')
    else:
        break
    iters = iters+1


