import reminders
import datetime

def bolus_reminder():
	r_bol = reminders.Reminder()
	r_post = reminders.Reminder()
	r_bol.title = 'Ya te diste el bolo? \n Empieza a comer.'
	r_post.title = 'Checar glc postprandial'
	
	bol = datetime.datetime.now() +\
	datetime.timedelta(minutes=5)
	
	post_prand =\
	  datetime.datetime.now() +\
	  datetime.timedelta(minutes=119)
	
	r_bol.due_date = bol
	r_post.due_date = post_prand
	
	a1 = reminders.Alarm()
	a2 = reminders.Alarm()
	a1.date = bol
	a2.date = post_prand
	
	r_bol.alarms = [a1]
	r_bol.save()
	r_post.alarms = [a2]
	r_post.save()
#

def hypo_remind():
	r = reminders.Reminder()
	r.title = '15 min desde hipoglucemia, volver a medir'
	due = datetime.datetime.now() +\
	   datetime.timedelta(minutes=15)
	r.due_date = due
	a = reminders.Alarm()
	a.date = due
	r.alarms = [a]
	r.save()
#
