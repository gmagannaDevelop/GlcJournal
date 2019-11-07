# IMPORTS:
import datetime as dt
import os
import ui
import console
import location

import wifi
import logger as log
import json as js
from Drive import Drive
from pathinit import Dir
#####################################


# FUNCTIONS:
def view_switch(sender):
	vs = sender.superview
	i = vs['seg1'].selected_index
	if i > 0:
		views[i].present(hide_title_bar=True)
		if i < 5:
			views[i]['timefield'].text = str(dt.datetime.now().time())[0:5]
		else:
			with open(os.path.join(_path,
				'journal.jl'), 'r') as f:
				lines = f.readlines()
				n = len(lines)
		

def close_subview(sender):
	vs = sender.superview
	views[0]['seg1'].selected_index = 0
	vs.close()
	show_wifi_status()
	show_journal_lines()


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
	if i != 4:
		j = view['table'].selected_row[1]
	entryType = {
		1: 'alarm',
		2: 'event',
		3: 'data',
		4: 'sensor'
	}
	carbs = as_int(view['carbsfield'].text) if view['carbsfield'] else None
	
	insulin = as_float(view['insulinfield'].text) if view['insulinfield'] else None
	
	food = format_food(view['foodfield'].text) if view['foodfield'] else None

	act_ins = as_float(view['actinsfield'].text) if view['actinsfield'] else None
	
	if i == 4:
		ref = view['reffield'].text if view['reffield'].text else None
		lot = view['lotfield'].text if view['lotfield'].text else None
		info = {
			'type': entryType[i],
			'dateTime': str(date),
			'REF': ref,
			'LOT': lot,
			'secondRound': view['recycle'].value,
			'initSuccess': view['success'].value,
			'location': location.get_location()
		}
	else:
		info = {
			'type': entryType[i],
			'dateTime': str(date),
			'IG': as_int(view['igfield'].text),
			'trend': as_int(view['trendfield'].text),
			'BG': as_int(view['bgfield'].text),
			'details': tables[i][j],
			'carbs': carbs,
			'insulin': insulin,
			'activeInsulin': act_ins,
			'food': food,
			'location': location.get_location()
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
	#dayif data['dateTime'] 
	#^ this if for implementing the postprandial alerts.
	file = _path + '/' + 'journal.jl'
	log_success = log.save(data, file)
	save_status_alert(log_success)
	if log_success:
		views[0]['label2'].text = 'Out of Sync'


@ui.in_background
def active_insulin(sender):
	''' Calculate the active 
	insulin at a desired time given the dose and bolus time.
	'''
	hour1 = console.input_alert('Bolus time')
	
	dose = float(console.input_alert('Dose'))
	
	hour2 = console.input_alert('Desired time')
	
	hour1 = dt.datetime.strptime(hour1, '%H:%M').time()
	
	hour2 = dt.datetime.strptime(hour2, '%H:%M').time()
	
	hour1 = dt.datetime.combine(dt.date.min, hour1) - dt.datetime.min
	
	hour2 = dt.datetime.combine(dt.date.min, hour2) - dt.datetime.min
	
	delta = hour2 - hour1
	mins = delta.total_seconds()//60
	
	active = (lambda t, d: d + (-d/180)*t if t < 180 else 0)(mins, dose)
	
	active = round(active, 2)
	
	console.alert(f'Active Insulin: {active}')


def last_n(ls: list, n: int):
	''' Return the last n elements of 
	a list, if n is less or equal than
	the list length. 
	Otherwise return the whole list.
	'''
	size = len(ls)
	if n <= size:
		return ls[size-n:size]
	else:
		return ls


def build_string(ls: list):
	''' Build a displayable string 
	from a list of dictionaries.
	'''
	my_string = ''
	for entry in ls:
		for key in entry.keys():
			my_string += f'{key}: {entry[key]}\n'
		my_string += '\n\n'
	return my_string


def format_food(s: str) -> list:
	if s:
		s = s.strip()
		s = s.lower()
		s = s.replace('.', '')
		allowed = [
			'a', 'e', 'i',
			'o', 'u', 'n',
			'c', 'e', 'a',
			'u', 'oe', 'o',
			'e', 'a', 'e'
		]
		forbidden = [
			'á', 'é', 'í',
			'ó', 'ú', 'ñ',
			'ç', 'è', 'à',
			'ù', 'œ', 'ô',
			'ê', 'â', 'ë'
		]
		for fo, al in zip(forbidden, allowed):
			s = s.replace(fo, al)
		s = s.split(',')
	else:
		s = None
	return s


def display_last(sender):
	vs = sender.superview
	x  = []
	try:
		# implement sorted boolean ! 
		chronological = vs['switch1'].value
		#n = int(vs['textfield1'].text)
	except:
		n = 1
	with open(os.path.join(_path, 'journal.jl'), 'r') as f:
		lines = f.readlines()
		for line in lines:
			x.append(js.loads(line))
			
	if chronological:
		# Display entries on chronological order :
		dates = [
			y['dateTime'] for y in x
		]
		s_dates = sorted(dates)
		idx = []
		for sdate in s_dates:
			idx += [
				j for j, date in\
				enumerate(dates)\
				if date == sdate
			]	
		x = [x[i] for i in idx]
	
	x.reverse()
	#x = last_n(x, n) # buggy
	
	vs['textview1'].text = build_string(x)


@ui.in_background
def sync(sender):
	wireless = wifi.is_connected()
	show_wifi_status()
	if wireless:
		views[0]['label2'].text = 'Connecting...'
		drive = Drive()
		updated = drive.update('journal.jl')
		sync_status_alert(updated)
		if updated:
			views[0]['label2'].text = 'All changes saved to Google Drive'
		else:
			views[0]['label2'].text = 'Out of Sync'
	else:
		console.alert('WiFi required for sync')
		
def show_journal_lines():
	if 'journal.jl' not in os.listdir(_path):
		open(os.path.join(_path, 'journal.jl'), 'a').close()
	with open(os.path.join(_path, 'journal.jl'), 'r') as f:
		lines = f.readlines()
		lines = len(lines)
	views[0]['lines'].text = str(lines)
			

def reload(sender):
	main()

###################################


def main():
	global _path
	_path = '/private/var/mobile/Containers/Shared/AppGroup/B4C4E9BD-48D0-410C-A4B9-F05626709C96/Pythonista3/Documents/GlcJournal'
	dir = Dir(_path)
	if not dir.cd_to_goal():
		raise Exception('Directory init failed.')
	
	global views
	views = [ 
		ui.load_view('multiview'),
		ui.load_view('Alarms'),
		ui.load_view('Events'),
		ui.load_view('Data'),
		ui.load_view('Sensor'),
		ui.load_view('Review')
	]
	
	if not dir.cd_to_goal():
		raise Exception('Directory init failed.')
	
	views[0]['journal'].text = str(
		'journal.jl' in os.listdir(_path)
		)
	
	if 'client_secrets.json' not in os.listdir():
		raise Exception('FATAL: client_secrets.json missing')
	
	if 'mycreds.txt' not in os.listdir():
		raise Exception('FATAL: Credentials missing')
	
	show_journal_lines()
	
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
			'Pre-Exercice',
			'Excercice',
			'Post-Exercice',
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
	views[0].present('sheet', hide_close_button=False)
	#console.alert('VERIFY JOURNAL')
	

if __name__ == '__main__':
	main()
	print()
