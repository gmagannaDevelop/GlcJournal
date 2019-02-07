# IMPORTS:
import datetime as dt
import ui
import console

import wifi
import logger as log
from Drive import Drive
from pathinit import Dir
#####################################


# FUNCTIONS:
def view_switch(sender):
	vs = sender.superview
	i = vs['seg1'].selected_index
	if i != 0:
		views[i].present(hide_title_bar=True)
		views[i]['timefield'].text = str(dt.datetime.now().time())[0:5]
		

def close_subview(sender):
	vs = sender.superview
	views[0]['seg1'].selected_index = 0
	vs.close()
	show_wifi_status()

def show_wifi_status():
	views[0]['label4'].text = str(wifi.is_connected())
	
def get_datetime(superview):
	i = views.index(superview)
	d = views[i]['datepicker1'].date.date()
	t = views[i]['timefield'].text
	t = dt.datetime.strptime(t, '%H:%M').time()
	d = dt.datetime.combine(d, t)
	return d
	
def as_int(string):
	try:
		x = int(string)
	except:
		x = None
	return x

def as_float(string):
	try:
		x = float(string)
	except:
		x = None
	return x
	
def get_info(view, date):
	i = views.index(view)
	j = view['table'].selected_row[1]
	entryType = {
		1: 'alarm',
		2: 'event',
		3: 'data'
	}
	carbs = as_int(view['carbsfield'].text) if view['carbsfield'] else None
	
	insulin = as_float(view['insulinfield'].text) if view['insulinfield'] else None
	
	food = as_int(view['foodfield'].text) if view['foodfield'] else None
	
	info = {
		'type': entryType[i],
		'dateTime': str(date),
		'IG': as_int(view['igfield'].text),
		'trend': as_int(view['trendfield'].text),
		'BG': as_int(view['bgfield'].text),
		'details': tables[i][j],
		'carbs': carbs,
		'insulin': insulin,
		'food': food
	}
	return info
	
@ui.in_background
def save_status_alert(success):
	if success:
		console.alert('Entry saved')
	else:
		console.alert('ERROR: Entry not saved')

@ui.in_background
def sync_status_alert(success):
	if success:
		console.alert('Successful Synchronization')
	else:
		console.alert('ERROR: Unsuccessful Synchronization')
		
def save_entry(sender):
	vs   = sender.superview
	date = get_datetime(vs)
	data = get_info(vs, date)
	log_success = log.save(data)
	save_status_alert(log_success)

@ui.in_background
def sync(sender):
	wireless = wifi.is_connected()
	show_wifi_status()
	if wireless:
		drive = Drive()
		x = drive.update('journal.jl')
		sync_status_alert(x)
		if x:
			views[0]['label2'].text = 'All changes saved to Google Drive'
		else:
			views[0]['label2'].text = 'Out of Sync'
	else:
		console.alert('WiFi required for sync')
	
###################################


def main():
	_path = '/private/var/mobile/Containers/Shared/AppGroup/B4C4E9BD-48D0-410C-A4B9-F05626709C96/Pythonista3/Documents/GlcJournal'
	dir = Dir(_path)
	if not dir.cd_to_goal():
		raise Exception
		
	#global drive 
	#drive = Drive()
	
	global views
	views = [ 
		ui.load_view('multiview'),
		ui.load_view('Alarms'),
		ui.load_view('Events'),
		ui.load_view('Data')
	]
	
	global tables 
	tables = [
		[],
		[ 
			'Alert before hyper',
			'Alert on hyper',
			'Alert before hypo',
			'Alert on hypo',
			'Suspension before hypo',
			'Basal resumption',
			'Fast increment' 
		],
		[ 
			'Postprandial',
			'Postcorrection',
			'Exercice',
			'Stress',
			'Rest',
			'Alcohol',
			'Sleep',
			'Wake'
		],
		[
			'Normal',
			'Dual',
			'Square'
		]
	]
	
	show_wifi_status()
	views[0].present('sheet', hide_close_button=True)


if __name__ == '__main__':
	main()
	print()
