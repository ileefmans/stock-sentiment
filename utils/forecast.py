from data import Stock
from datetime import datetime






def get_interval():
	weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	day = weekdays[datetime.today().weekday()]

	if day in ['Saturday', 'Sunday']:


	else:
