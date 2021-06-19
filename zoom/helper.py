from zoom.models import StoreData,CurrentMeetinglog,ReportLog,AuthIds
import time as time_import
from datetime import datetime

def time(t,date):
    l = t.split(":")
    l[0] = str(int(l[0])+5)
    l[1] = str(int(l[1])+30)
    if(int(l[1])>=60):
        l[0] = str(int(l[0])+1)
        l[1] = str(int(l[1])-60)
    if(int(l[0])<10):
        l[0] = '0'+l[0]
    if(int(l[1])<10):
        l[1] = '0'+l[1]
    if(int(l[0])>=24):
        l[0] = str(int(l[0])-24)
        if(int(l[0])<10):
            l[0] = '0'+l[0]
        d = date.split('-')
        if (int(d[2])+1) < 10:
            date = d[0]+ '-'+d[1]+'-'+'0'+str(int(d[2])+1)
        else:
            date = d[0]+ '-'+d[1]+'-'+str(int(d[2])+1)
    return date,str(l[0]+":"+l[1]+":"+l[2])

def onlytime(t):
    l = t.split(":")
    l[0] = str(int(l[0])+5)
    l[1] = str(int(l[1])+30)
    if(int(l[1])>=60):
        l[0] = str(int(l[0])+1)
        l[1] = str(int(l[1])-60)
    if(int(l[0])<10):
        l[0] = '0'+l[0]
    if(int(l[1])<10):
        l[1] = '0'+l[1]
    if(int(l[0])>=24):
        l[0] = str(int(l[0])-24)
        if(int(l[0])<10):
            l[0] = '0'+l[0]
    return str(l[0]+":"+l[1]+":"+l[2])


def ismeetingon():
    a = StoreData.objects.filter(event = 'meeting.ended')
    b = StoreData.objects.filter(event = 'meeting.started')
    starttime_a = []
    for i in a:
        starttime_a.append(i.starttime)
    starttime_b = []
    for i in b:
        starttime_b.append(i.starttime)

    if(len(a)==len(b)):
        return 'no'
    else:
        missing_time = ""
        for i in starttime_b:
            flag = 0
            for j in starttime_a:
                if i == j:
                    flag=1
                    break
            if flag == 0:
                missing_time = i
                break
        return(missing_time)


def altercurrentmeetinglog_add(starttime,startdate,auth,topic):
    a = CurrentMeetinglog.objects.filter(authtoken=auth,starttime=starttime,startdate=startdate)
    if len(a)==0:
        inst = CurrentMeetinglog(authtoken=auth,starttime=starttime,startdate=startdate,topic=topic)
        inst.save()
    else:
        CurrentMeetinglog.objects.filter(authtoken=auth,starttime=starttime,startdate=startdate).delete()
        inst = CurrentMeetinglog(authtoken=auth,starttime=starttime,startdate=startdate,topic=topic)
        inst.save()

def altercurrentmeetinglog_delete(starttime,startdate,auth):
    CurrentMeetinglog.objects.filter(authtoken=auth,starttime=starttime,startdate=startdate).delete()



def generate_report(starttime,startdate,auth,endtime,topic):
    flag=0
    try:
        query_checkstart = CurrentMeetinglog.objects.filter(authtoken=auth,starttime=starttime,startdate=startdate)
        if len(query_checkstart) == 0:
            flag=1
    except:
        flag=1
    if flag == 1:
        return -1

    try:
        query_joined = StoreData.objects.filter(authtoken=auth,starttime=starttime, startdate=startdate, event='meeting.participant_joined')
        query_left = StoreData.objects.filter(authtoken=auth,starttime=starttime, startdate=startdate, event='meeting.participant_left')

        FMT = '%H:%M:%S'
        report = []

        users = []
        for object in query_joined:
            users.append(object.username)
        users = set(users)
        duration = get_difftime(endtime,starttime)


        for user in users:
            query_user_join = query_joined.filter(username=user)
            query_user_left = query_left.filter(username=user)
            time_user = []
            for object in query_user_join:
                time_user.append(object.jointime)
            for object in query_user_left:
                time_user.append(object.jointime)
            sorted_time = sorttime(sorted((time_import.strptime(d, "%H:%M:%S") for d in time_user), reverse=False))
            first_join_time = sorted_time[0]
            last_leave_time = sorted_time[len(sorted_time)-1]
            no_of_times_left = (len(sorted_time)/2) -1
            duration_out = 0.0
            for times_counter in range(0,int(len(sorted_time)/2)+1,2):
                duration_out += get_difftime(sorted_time[times_counter+1],sorted_time[times_counter])
            dict_object = {'name':user,
                           'firstjoined':first_join_time,
                           'timeleft':last_leave_time,
                           'numberoftimesleft':int(no_of_times_left),
                           'duration':int(duration_out)}
            report.append(dict_object)

        final_dict = {'duration':duration,'report':report,'endtime':endtime}
        u = AuthIds.objects.filter(authtoken=auth)
        user = u.get().username
        ReportLog.objects.create(username = user, starttime=starttime, startdate=startdate, topic=topic, report=str(final_dict))

    except Exception as e:
        print(e)


def get_difftime(t1,t2):
    t1 = t1.split(':')
    t2 = t2.split(':')
    m1 = int(t1[0])*60 + int(t1[1])
    m2 = int(t2[0])*60 + int(t2[1])
    d = m1-m2
    return d

def sorttime(time_list):
    new = []
    for i in range(0,len(time_list)):
        h = str(time_list[i].tm_hour)
        if(int(h)<10):
            h = '0' + h
        m = str(time_list[i].tm_min)
        if(int(m)<10):
            m = '0' + m
        s = str(time_list[i].tm_sec)
        if(int(s)<10):
            s = '0' + s
        new.append(h+":"+m+":"+s)
    return new
