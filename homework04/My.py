from age import age_predict
from api import messages_get_history, get_friends
from messages import count_dates_from_messages, plotly_messages_freq
from api_models import Message
from network import get_network, plot_graph


print(age_predict(155393609))
history = messages_get_history(155393609, count=300)
mlist = [Message(**mes) for mes in history]
dates = count_dates_from_messages(mlist)
plotly_messages_freq(dates[0], dates[1])

friends = get_friends(155393609, fields='bdate')['response']['items']
ids = []
names = []
for friend in friends:
    ids.append(friend['id'])
    names.append(friend['first_name'] + ' ' + friend['last_name'])
edges = get_network(ids)
plot_graph(edges, names)
