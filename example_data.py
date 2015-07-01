import pickle

from library.event import *

event = Event("MoaL", "Brian & Kofi", "March")
venue = Tournament(event, 'Venue', 1)
singles = Tournament(event, 'Singles', 1)
doubles = Tournament(event, 'Doubles', 1, team=True)
mord = Entrant(event, 'Brian Lester', 'Mordicon', 'PGH')
kofi = Entrant(event, 'Kofi Osei', 'Kofi', 'PGH')
bean = Entrant(event, 'Carmen C', 'Beanwolf', 'PGH')
pillz = Entrant(event, 'Sam', 'Pillz', 'OU')
Tournament_Entrant(venue, mord)
Tournament_Entrant(singles, mord)
Tournament_Entrant(doubles, mord, 'Kofi')

Tournament_Entrant(venue, kofi)
Tournament_Entrant(singles, kofi)
Tournament_Entrant(doubles, kofi, 'Mordicon')

Tournament_Entrant(venue, bean)
Tournament_Entrant(singles, bean)

Tournament_Entrant(venue, pillz)

for i in event.tournaments.tournaments:
  for j in i.entrants:
    print j.name
  
pickle.dump(event, open('event.pkl', 'wb'), -1)