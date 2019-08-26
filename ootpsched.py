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

# To spread out the days off, we try to avoid scheduling a divdiv series
# for the same division three times in a row.
def search_for_blackout_div(dates,current_date):
    blackoutdiv = 'NoBlackout'
    divisions_playing = set()
    for r in range(current_date,0,-1):
        d = dates[r]
        for s in d.serieslist:
            if s.seriestype == 'divdiv':
                if s.homediv in divisions_playing:
                    return s.homediv
                else:
                    divisions_playing.add(s.homediv)
                if s.awaydiv in divisions_playing:
                    return s.awaydiv
                else:
                    divisions_playing.add(s.awaydiv)
    return 'NoBlackout'

def assigndivdiv(dates,series):
    for r in range(0,len(dates)):
        d = dates[r]
        if d.length == 4 and d.datetype == 'weekend':
            blackout = search_for_blackout_div(dates,r)
            print('Blackout division for '+str(d)+' is '+blackout)
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
        elif d.length >= 3:
            blackout = search_for_blackout_div(dates,r)
            print('Blackout division for '+str(d)+' is '+blackout)
            try:
                divdivseries = popdivdivseries(series,3,blackout)
            except:
                print('Unable to find a series not containing the '+blackout+' division on '+str(d))
                continue
            print('Assigning :'+str(divdivseries))
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
    for d in range(0,len(schedule)):
        print(format_date(d)+': '+str(schedule[d]))

def print_series_dates(dates):
    for s in dates:
        print(str(s.startdate)+':('+str(s.length)+'):'+str(s.serieslist))

        
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
    print_schedule(gamedays)
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
                if streak > 21:
                    firstdate=openingday(year)+timedelta(d-streak)
                    firststr=firstdate.strftime('%a')+' '+str(firstdate)
                    lastdate=openingday(year)+timedelta(d-1)
                    laststr=lastdate.strftime('%a')+' '+str(lastdate)
                    print(thisteam+' plays '+str(streak)+' consecutive games starting '+firststr+' and ending '+laststr)
                if prevstreak > 0 and prevstreak+streak < 21:
                    print('----> Good day for inserting a game')
                    for g in schedule[d-1]:
                        if g[0] == thisteam or g[1] == thisteam:
                            print(g)
                    for g in schedule[d+1]:
                        if g[0] == thisteam or g[1] == thisteam:
                            print(g)
                prevstreak=streak
                streak=0
                offday=openingday(year)+timedelta(d)
                offdaystr=offday.strftime('%a')+' '+str(offday)
                print(thisteam+' has an off day on '+offdaystr)

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
                if prevstreak > 0 and prevstreak+streak < 21:
                    teamsavailabletoplayonthisoffday[prev].add(thisteam)
                prev = d
                prevstreak = streak
                streak = 0
        if prevstreak > 0 and prevstreak+streak < 21:
            teamsavailabletoplayonthisoffday[prev].add(thisteam)
    for d in range(0,len(teamsavailabletoplayonthisoffday)):
        if len(teamsavailabletoplayonthisoffday[d]):
            offday=openingday(year)+timedelta(d)
            offdaystr=offday.strftime('%a')+' '+str(offday)
            print('The following teams can have a game added to current off day '+format_date(d)+':') 
            print('.... '+str(teamsavailabletoplayonthisoffday[d]))
    return teamsavailabletoplayonthisoffday

def schedule_contains_matchup(schedule,d,team1,team2):
    for g in schedule[d]:
        if g[0] == team1 and g[1] == team2:
            return True
    return False

def find_open_day_to_move_game_to(schedule,date_to_free_up,matchup,fixupdays):
    for d in range(0,len(fixupdays)):
        if matchup[0] in fixupdays[d] and matchup[1] in fixupdays[d]:
            print(matchup[0]+' and '+matchup[1]+' both are available on '+format_date(d))
            if (schedule_contains_matchup(schedule,d-1,matchup[0],matchup[1]) or
                schedule_contains_matchup(schedule,d+1,matchup[0],matchup[1]) ):
                print('Moving game between '+matchup[0]+' and '+matchup[1]+' from '+
                      format_date(date_to_free_up)+' to '+format_date(d))
                schedule[date_to_free_up].remove(matchup)
                schedule[d].append(matchup)
                return True
    return False

def find_and_make_series_swap(schedule,date_to_free_up,matchup,fixupdays):
    print('=====')
    for d in range(0,len(fixupdays)):
        if matchup[0] in fixupdays[d] and matchup[1] in fixupdays[d]:
            print(matchup[0]+' and '+matchup[1]+' both are available on '+format_date(d))
            if schedule_contains_matchup(schedule,d-1,matchup[1],matchup[0]):
                to_series_count=1
                while schedule_contains_matchup(schedule,d-1-to_series_count,matchup[1],matchup[0]):
                    to_series_count=to_series_count+1
                print('..and they play in a '+str(to_series_count)+' game series in other stadium on '+format_date(d-to_series_count))
                if schedule_contains_matchup(schedule,date_to_free_up+1,matchup[0],matchup[1]):
                    from_series_count=2
                    while schedule_contains_matchup(schedule,date_to_free_up+from_series_count,matchup[0],matchup[1]):
                        from_series_count=from_series_count+1
                    if (from_series_count == to_series_count+1):
                        print('....to be swapped with a '+str(from_series_count)+' game series starting on '+format_date(date_to_free_up))
                        return True
                elif schedule_contains_matchup(schedule,date_to_free_up-1,matchup[0],matchup[1]):
                    from_series_count=2
                    while schedule_contains_matchup(schedule,date_to_free_up-from_series_count,matchup[0],matchup[1]):
                        from_series_count=from_series_count+1
                    if (from_series_count == to_series_count+1):
                        print('....to be swapped with a '+str(from_series_count)+' game series starting on '+format_date(date_to_free_up-from_series_count+1))
                        return True
    return False

def get_matchup_for_team(schedule,d,thisteam):
    for t in schedule[d]:
        if t[0] == thisteam or t[1] == thisteam:
            return t
    
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
                if streak > 21:
                    firstd = max(d-22,d-streak+3)
                    lastd = min(d-streak+22,d-3)
                    print(thisteam+' plays '+str(streak)+' consecutive games starting '+format_date(d-streak)+' and ending '+format_date(d-1))
                    print('Need to create an open date between '+format_date(firstd)+' and '+format_date(lastd-1))
                    for i in range(firstd,lastd):
                        dayofweek=get_day_of_week(i)
                        if dayofweek in ['Mon', 'Wed', 'Thu']:
                            if isaholiday(openingday()+timedelta(i)):
                                print(format_date(i)+' is a holiday')
                                continue
                            m = get_matchup_for_team(schedule,i,thisteam)
                            print('Search for a swap date for '+str(m)+' on '+format_date(i))
                            if find_open_day_to_move_game_to(schedule,i,m,fixupdays):
                                return True
                            #if find_and_make_series_swap(schedule,i,m,fixupdays):
                            #    return True
                    print('Unable to create an open date between '+format_date(firstd)+' and '+format_date(lastd-1))
                    return False
                prevstreak=streak
                streak=0
    return False
                
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

    assignthreegameweekdayroundrobin(allseriesdates,allseries)
    if (len(allseries)):
        print(str(len(series))+' series were not assigned.')
        return False

    print()
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
        print(str(s.startdate)+':('+str(s.length)+'):'+str(s.serieslist))

    print()
    print()
    if check_series_length(allseriesdates):
        print_series_dates(allseriesdates)
        return False

    schedule = assigngamestodates(allseriesdates)
    print()
    print()
    #try:
    fix_consecutive_offdays(schedule)
    #except:
    #    print('Failure during fix_consecutive_offdays')
    #    return False
    offdayfixuplist = create_offday_fixup_list(schedule)
    while find_and_fix_long_streak(schedule,offdayfixuplist):
        continue
    print()
    print()
    #print_schedule(schedule)
    #check_for_offdays(schedule)
    return True

random.seed(1)
allseriesdates = initializeseriesdates()
matchups = initializematchups()
allseries = initializeseries()
if not create_schedule(allseriesdates,allseries):
    print('Schedule creation failed.  See above messages for details.')

