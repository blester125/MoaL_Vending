import pickle

event = pickle.load(open('event.pkl', 'rb'))

for i in event.tournaments:
  for j in i.entrants:
    print j.name