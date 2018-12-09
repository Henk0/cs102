from age import age_predict
from api import messages_get_history
from messages import count_dates_from_messages, plotly_messages_freq
from api_models import Message

print(age_predict(150758309))
history = messages_get_history(150758309, count=300)
mlist = [Message(**mes) for mes in history]
print(mlist)
dates = count_dates_from_messages(mlist)
print(dates)
plotly_messages_freq(dates[0], dates[1])
