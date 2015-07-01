class Event(object):
  def __init__(self, name='', TO='', date=''):
    self.name = name
    self.TO_name = TO
    self.date = date
    self.number_of_entrants = 0 
    self.tournaments = Tournaments()
    self.entrants = Entrants()
 
  def add_tournament(self, tournament):
    self.tournaments.add_tournament(tournament)

  def get_entrants(self):
    return self.number_of_entrants

  def add_entrant(self, entrant):
    self.number_of_entrants += 1
    self.entrants.add_entrant(entrant)

class Entrants(object):
  def __init__(self):
    self.name = 'Entrants'
    self.entrants = []

  def add_entrant(self, entrant):
    self.entrants.append(entrant)

class Entrant(object):
  def __init__(self, event, name='', tag='', location=''):
    self.name = name
    self.tag = tag
    event.add_entrant(self)
    self.number = event.get_entrants()
    self.amount_owed = 0
    self.location = location
    self.tournaments = []
    self.tournaments_parents = []

  def add_tournament(self, tournament):
    self.tournaments.append(tournament)
    self.tournaments_parents.append(tournament.parent)
    self.amount_owed += tournament.price

class Tournaments(object):
  def __init__(self):
    self.name = 'Tournaments'
    self.tournaments = []

  def add_tournament(self, tournament):
    self.tournaments.append(tournament)

class Tournament(object):
  """Data about a tournament at an event.
   
  To be added to event.tournaemts

  """
  def __init__(self, event, name, price, team=False):
    self.name = name
    self.price = price
    self.total = 0
    self.team = team
    event.add_tournament(self)
    self.entrants = []

  def add_entrant(self, entrant):
    self.entrants.append(entrant)

class Tournament_Entrant(Tournament):
  """Data about a tournament but specific to an entrant.

  Parent is the Tournament that this is part of.

  To be added to entrant.tournaments

  """
  def __init__(self, parent, entrant, teammate=''):
    self.name = parent.name
    self.parent = parent
    self.price = parent.price
    self.team = parent.team
    self.teammate = teammate
    entrant.add_tournament(self)
    self.parent.add_entrant(entrant)