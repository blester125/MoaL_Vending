from library.excel import *
from library.event import *

event = Event("DICK","BUTT","MARCH")
excel = Workbook()
venue = Tournament(event, "Venue", 1)
Doubles = Tournament(event, "Dubs", 1)
entrant = Entrant(event, "EXAMPLE", "NUTZ", "PGH")
NUTZ_venue = Tournament_Entrant(venue, entrant)
Nutz_dubs = Tournament_Entrant(Doubles, entrant)
excel.save_tournament_data(event)
excel.save_entrant_data(event, entrant)
excel.save_workbook(event)