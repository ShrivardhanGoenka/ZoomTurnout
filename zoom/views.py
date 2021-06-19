from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from zoom.models import StoreData,CurrentMeetinglog,AuthIds,Files,ReportLog,Metrics
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .helper import time,altercurrentmeetinglog_delete,altercurrentmeetinglog_add,generate_report,onlytime,get_difftime
from datetime import datetime
# Create your views here.
@csrf_exempt
def zoom(request):
    try:
        if request.method == 'POST':
            a = request.body
            b = eval(a.decode('ASCII'))
            auth = request.headers['Authorization']
            startdate, starttime = time(b['payload']['object']['start_time'].split('T')[1].split('Z')[0],
                                         b['payload']['object']['start_time'].split('T')[0])
            if b['event'] == "meeting.participant_joined":
                instance = StoreData.objects.create(username = b['payload']['object']['participant']['user_name'],
                                            email = b['payload']['object']['participant']['email'],
                                            jointime = onlytime(b['payload']['object']['participant']['join_time'].split('T')[1].split('Z')[0]),
                                            user_id = b['payload']['object']['participant']['id'],
                                            event = b['event'],
                                            uiud = b['payload']['object']['uuid'],
                                            topic = b['payload']['object']['topic'],
                                            starttime = starttime,
                                            startdate = startdate,
                                            authtoken = auth)
            elif b['event'] == "meeting.participant_left":
                instance = StoreData.objects.create(username = b['payload']['object']['participant']['user_name'],
                                            email = b['payload']['object']['participant']['email'],
                                            jointime = onlytime(b['payload']['object']['participant']['leave_time'].split('T')[1].split('Z')[0]),
                                            event = b['event'],
                                            uiud = b['payload']['object']['uuid'],
                                            topic = b['payload']['object']['topic'],
                                            starttime = starttime,
                                            startdate = startdate,
                                            authtoken = auth)
            elif (b['event'] == "meeting.started"):
                instance = StoreData.objects.create(event = b['event'],
                                            topic = b['payload']['object']['topic'],
                                            starttime = starttime,
                                            startdate = startdate,
                                            authtoken = auth)
                altercurrentmeetinglog_add(starttime = starttime,
                                            startdate = startdate,
                                            auth = auth,
                                            topic = b['payload']['object']['topic'])
            elif b['event'] == "meeting.ended":
                instance = StoreData.objects.create(event = b['event'],
                                            topic = b['payload']['object']['topic'],
                                            starttime = starttime,
                                            startdate = startdate,
                                            jointime = onlytime(b['payload']['object']['end_time'].split('T')[1].split('Z')[0]),
                                            authtoken = auth)

                generate_report(starttime,
                                startdate,
                                auth,
                                endtime=onlytime(b['payload']['object']['end_time'].split('T')[1].split('Z')[0]),
                                topic= b['payload']['object']['topic'])
                altercurrentmeetinglog_delete(starttime = starttime,
                                            startdate = startdate,
                                            auth = auth)
            else:
                instance = StoreData.objects.create(username = b['payload']['object']['participant']['user_name'],
                                            email = b['payload']['object']['participant']['email'],
                                            jointime = onlytime(b['payload']['object']['participant']['date_time'].split('T')[1].split('Z')[0]),
                                            event = b['event'],
                                            uiud = b['payload']['object']['uuid'],
                                            topic = b['payload']['object']['topic'],
                                            starttime = starttime,
                                            startdate = startdate,
                                            authtoken = auth)
    except Exception as e:
        print('Exception:'+str(e) )

    return render(request,'index.html')

@login_required
def currentmeeting(request):
    try:
        u = AuthIds.objects.filter(username = request.user.username)
        auth = u.get().authtoken
        query = CurrentMeetinglog.objects.filter(authtoken = auth)
        print(query)
        if len(query) == 1:
            joinquery = StoreData.objects.filter(starttime=query.get().starttime, startdate= query.get().startdate, authtoken = auth, event='meeting.participant_joined')
            list = []
            for object in joinquery:
                list.append(object.username)
            list = set(list)
            present = []
            left = []
            for i in list:
                mainquery_join = StoreData.objects.filter(starttime=query.get().starttime,
                                                          startdate= query.get().startdate,
                                                          authtoken = auth, event='meeting.participant_joined',
                                                          username = i)
                mainquery_left = StoreData.objects.filter(starttime=query.get().starttime,
                                                          startdate= query.get().startdate,
                                                          authtoken = auth,
                                                          event='meeting.participant_left',
                                                          username=i)
                print(i)
                if len(mainquery_left) < len(mainquery_join):
                    present.append(i)
                else:
                    left.append(i)
            files = []
            try:
                query_files = Files.objects.filter(username=request.user.username)
                for i in query_files:
                    files.append(i.name)
            except:
                pass
            if request.method == 'POST':
                query_content = Files.objects.filter(username=request.user.username, name=request.POST.get('file'))
                names = query_content.get().content.split(',')

                absentees = []
                extra = []
                for n in names:
                    flag=0
                    for i in present:
                        try:
                            if(i.lower() == n.lower() or (i.lower().split(' ')[1]+' ' +i.lower().split(' ')[0])==n.lower()):
                                flag=1
                                break
                        except:
                            extra.append(i)
                    if flag==0:
                        absentees.append(n)

                for n in present:
                    flag=0
                    for i in names:
                        try:
                            if(i.lower() == n.lower() or (i.lower().split(' ')[1]+' ' +i.lower().split(' ')[0])==n.lower()):
                                flag=1
                                break
                        except:
                            extra.append(n)
                    if flag==0:
                        extra.append(n)

                return render(request,'zoom/currentmeeting.html',
                             {'meeting':True,
                              'nparticipants':len(present),
                              'starttime': query.get().starttime ,
                              'startdate': query.get().startdate,
                              'topic':query.get().topic,
                              'present':present,
                              'left':left ,
                              'files':files,
                              'attendance':True,
                              'absentees':set(absentees),
                              'extra':set(extra)})


            return render(request,'zoom/currentmeeting.html',
                         {'meeting':True,
                         'nparticipants':len(present),
                         'starttime': query.get().starttime ,
                         'startdate': query.get().startdate,
                         'topic':query.get().topic,
                         'present':present,
                         'left':left ,
                         'files':files,
                         'attendance':False})
        elif len(query)>1:
            list = []
            for object in query:
                dict = {'topic':object.topic, 'Created': (object.startdate+''+object.starttime), 'time':object.starttime, 'date':datetime.strptime(object.startdate, '%Y-%m-%d')}
                list.append(dict)
            return render(request,'zoom/multiple.html',{'list':list})
        else:
            return render(request,'zoom/currentmeeting.html',{'meeting':False})
    except Exception as e:
        print(e)
        return render(request,'zoom/current_meeting_invalidauthid.html')


@login_required
def currentmeeting_condition(request,name):
    startdate = name[:10]
    starttime = name[10:]
    u = AuthIds.objects.filter(username = request.user.username)
    auth = u.get().authtoken
    query = CurrentMeetinglog.objects.filter(authtoken = auth,startdate=startdate, starttime = starttime)
    if(len(query)==1):
        joinquery = StoreData.objects.filter(starttime=query.get().starttime, startdate= query.get().startdate, authtoken = auth, event='meeting.participant_joined')
        list = []
        for object in joinquery:
            list.append(object.username)
        list = set(list)
        present = []
        left = []
        for i in list:
            mainquery_join = StoreData.objects.filter(starttime=query.get().starttime,
                                                      startdate= query.get().startdate,
                                                      authtoken = auth, event='meeting.participant_joined',
                                                      username = i)
            mainquery_left = StoreData.objects.filter(starttime=query.get().starttime,
                                                      startdate= query.get().startdate,
                                                      authtoken = auth,
                                                      event='meeting.participant_left',
                                                      username=i)
            print(i)
            if len(mainquery_left) < len(mainquery_join):
                present.append(i)
            else:
                left.append(i)
        files = []
        try:
            query_files = Files.objects.filter(username=request.user.username)
            for i in query_files:
                files.append(i.name)
        except:
            pass
        if request.method == 'POST':
            query_content = Files.objects.filter(username=request.user.username, name=request.POST.get('file'))
            names = query_content.get().content.split(',')

            absentees = []
            extra = []
            for n in names:
                flag=0
                for i in present:
                    try:
                        if(i.lower() == n.lower() or (i.lower().split(' ')[1]+' ' +i.lower().split(' ')[0])==n.lower()):
                            flag=1
                            break
                    except:
                        extra.append(i)
                if flag==0:
                    absentees.append(n)

            for n in present:
                flag=0
                for i in names:
                    try:
                        if(i.lower() == n.lower() or (i.lower().split(' ')[1]+' ' +i.lower().split(' ')[0])==n.lower()):
                            flag=1
                            break
                    except:
                        extra.append(n)
                if flag==0:
                    extra.append(n)

            return render(request,'zoom/currentmeeting_condition.html',
                         {'meeting':True,
                          'nparticipants':len(present),
                          'starttime': query.get().starttime ,
                          'startdate': query.get().startdate,
                          'topic':query.get().topic,
                          'present':present,
                          'left':left ,
                          'files':files,
                          'name':name,
                          'attendance':True,
                          'absentees':set(absentees),
                          'extra':set(extra)})


        return render(request,'zoom/currentmeeting_condition.html',
                     {'meeting':True,
                     'nparticipants':len(present),
                     'name':name,
                     'starttime': query.get().starttime ,
                     'startdate': query.get().startdate,
                     'topic':query.get().topic,
                     'present':present,
                     'left':left ,
                     'files':files,
                     'attendance':False})
    else:
        return render(request,'zoom/currentmeeting.html',{'meeting':False,'report':True})



def reports(request):
    a = ReportLog.objects.filter(username=request.user.username)
    list = []
    for object in a:
        dict = {'topic':object.topic, 'Created': (object.startdate+''+object.starttime), 'time':object.starttime, 'date':datetime.strptime(object.startdate, '%Y-%m-%d')}
        list.append(dict)
    sortedArray = sorted(list,key=lambda x: datetime.strptime(x['Created'], '%Y-%m-%d%H:%M:%S'), reverse=True)
    s= False
    if len(list) >0:
        s = True
    return render(request,'zoom/reports.html',{'size':s, 'list':sortedArray})

def viewreport(request,name):
    try:
        date = name[:10]
        time = name[10:]
        query = ReportLog.objects.filter(username=request.user.username,starttime=time,startdate=date)
        if len(query) == 0:
            return render(request,'zoom/viewreport.html',{'report':False})
        report = query.get().report
        report = eval(report)
        endtime = report['endtime']
        duration = report['duration']
        meetingdetails = {'duration':duration,
                            'starttime':time,
                            'startdate':date,
                            'topic': query.get().topic,
                            'endtime':report['endtime']}
        flagged = []
        flagged_late = []
        flagged_early = []
        flagged_duration = []
        query_metrics = Metrics.objects.filter(username=request.user.username)
        late = int(query_metrics.get().late)
        early = int(query_metrics.get().leftearly)
        duration = int(query_metrics.get().minduration)
        for object in report['report']:
            time_late = get_difftime(object['firstjoined'], time)
            time_early = get_difftime(endtime,object['timeleft'])
            if time_late >= late:
                dict = {'name':object['name'],'reason':('Was late to the meeting. Join time: ' + object['firstjoined']) }
                dic = {'name':object['name'],'late':time_late,'jointime' : object['firstjoined']}
                flagged_late.append(dic)
                flagged.append(dict)
            if time_early >= early:
                dict = {'name':object['name'],'reason':('Left the meeting early. Leave time: ' + object['timeleft']) }
                dic = {'name':object['name'],'leavetime':object['timeleft'],'early':time_early}
                flagged_early.append(dic)
                flagged.append(dict)
            if int(object['duration']) < duration:
                dict = {'name':object['name'],'reason':('Duration spent in meeting was inadequate. Duration in meeting: ' + str(object['duration']) + ' minutes') }
                dic = {'name':object['name'], 'duration':object['duration']}
                flagged_duration.append(dic)
                flagged.append(dict)

        files = []
        try:
            query_files = Files.objects.filter(username=request.user.username)
            for i in query_files:
                files.append(i.name)
        except:
            pass
        try:
            if request.method == 'POST':
                query_content = Files.objects.filter(username=request.user.username, name=request.POST.get('file'))
                names = query_content.get().content.split(',')

                absentees = []
                extra = []
                for n in names:
                    flag=0
                    for object in report['report']:
                        i = object['name']
                        try:
                            if(i.lower() == n.lower() or (i.lower().split(' ')[1]+' ' +i.lower().split(' ')[0])==n.lower()):
                                flag=1
                                break
                        except:
                            extra.append(i)
                    if flag==0:
                        absentees.append(n)

                for object in report['report']:
                    n = object['name']
                    flag=0
                    for i in names:
                        try:
                            if(i.lower() == n.lower() or (i.lower().split(' ')[1]+' ' +i.lower().split(' ')[0])==n.lower()):
                                flag=1
                                break
                        except:
                            extra.append(i)
                    if flag==0:
                        extra.append(n)

                flagged_attendance = []


                return render(request,'zoom/viewreport.html',{'report':True,
                                                              'meeting':meetingdetails,
                                                              'report':report['report'] ,
                                                              'flagged':flagged,
                                                              'flagged_late':flagged_late,
                                                              'flagged_early':flagged_early,
                                                              'flagged_duration':flagged_duration,
                                                              'files':files,
                                                              'absentees':set(absentees),
                                                              'attendance':True,
                                                              'path':name,
                                                              'extra':set(extra)})

        except Exception as e:
            print(e)



        return render(request,'zoom/viewreport.html',{'report':True,
                                                      'meeting':meetingdetails,
                                                      'report':report['report'] ,
                                                      'flagged':flagged,
                                                      'flagged_late':flagged_late,
                                                      'flagged_early':flagged_early,
                                                      'flagged_duration':flagged_duration,
                                                      'files':files,
                                                      'path':name})
    except Exception as e:
        print(e)
        return render(request,'zoom/viewreport.html',{'report':False})

    return render(request,'zoom/viewreport.html',{'report':False})

def viewreport_norequest(request):
    return render(request,'zoom/viewreport.html',{'report':False})
