import requests, random, time, traceback, itertools, math, sys
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pytz
plotly.tools.set_credentials_file(username='niksavilov', api_key='Qxc4TAOOwk8CU1os7wNx')
global access_token
global tz
tz = ''
access_token = '28e237e0c7934f94028c0e66ed9ffda21e2d49388f57070549425cdcfb909770dd755e971d383b97cbb76'
def get(url, params={}, timeout=5, max_retries=5, backoff_factor=1.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 1
    retries = 0
    while retries < max_retries:
        try:
            retries+=1
            response = requests.get(url, timeout = timeout)
            if response.ok:
                break
            else:
                print("delay ", delay)
                time.sleep(delay)
                delay = backoff_factor * delay + random.gauss(delay * 0.1, 1)
        except requests.exceptions.RequestException:
            print("Ooops. Err {err} occured. Sleep: {delay}".format(delay = delay, err = traceback.format_exception_only()))
            time.sleep(delay)
            delay = backoff_factor * delay + random.gauss(delay * 0.8, 0.8)
    if response.ok:
    	print('response was accepted')
    	return response
    else:
    	print('response wasnt accepted')
    	return('error') 
def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"    
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    # access_token = 'ffb882a0affcbaadecfc56f7cbeeac328fded8f4c01f59d2981c46643fa9e1151ed2f865c11fb1fe64566'
    # user_id = 141839173

    query_params = {
    'domain' : domain,
    'access_token': access_token,
    'user_id': user_id,
    'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = get(query)
    try:
        return response.json()['response']
    except:
        print("Invalid user id or access_token")
        sys.exit(1)
def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    summa = datetime.datetime.now() - datetime.datetime.now()
    count = 0
    for item in get_friends(user_id,'bdate')['items']:
    	s = item.get('bdate', '0')
    	if len(s) >= 8:
            print(s,item.get('first_name'),item.get('last_name'))
            age = datetime.datetime.now() - datetime.datetime.strptime(s,"%d.%m.%Y")
            summa += age
            count += 1
    return round(int(summa.days)/(365*count))
def messages_get_history(user_id, offset=0, count=200):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "offset must be positive integer"
    assert count >= 0, "count must be positive integer"
    domain = "https://api.vk.com/method"
    # user_id = 141839173

    query_params = {
    'domain' : domain,
    'access_token': access_token,
    'user_id': user_id,
    'count' : count,
    'offset' : offset
    }

    query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v=5.53".format(**query_params)
    response = get(query)
    try:
        return response.json()['response']
    except:
        print("Invalid user id or access_token")
        exit(1)
def messages_aggregator(user_id):
    offset = 0
    messages = []
    while True:
        response = messages_get_history(user_id = user_id, offset = offset)
        if response['items']:
            for g in response['items']:
                messages.append(g)
        else:
            return messages
        offset += 200
        time.sleep(0.4)
def count_dates_from_messages(messages):
    dates_arr = []
    for k in messages:
        date = datetime.datetime.fromtimestamp(k['date']).strftime("%Y.%m.%d")
        dates_arr.append(date)
    dates_list = list(set(dates_arr))
    frequency = []
    for j in dates_list:
        frequency.append({'date' : j, 'messages' : dates_arr.count(j)})
        # print({'date' : j, 'messages' : dates_arr.count(j)})
    frequency_sorted = sorted(frequency, key = lambda x: x['date'])
    return frequency_sorted
def plot_maker(dates_list):
    x = []
    y = []
    for j in dates_list:
        x.append(datetime.datetime.strptime(j.get('date'),"%Y.%m.%d").replace(tzinfo= pytz.utc))
        y.append(j.get('messages'))
    data = [go.Scatter(x = x, y = y)]
    py.plot(data)
    pass
    
def get_network(users_ids, as_edgelist=True):
    """ Building a friend graph for an arbitrary list of users """
    # PUT YOUR CODE HERE
    pass

# Example requests:
# plot_maker(count_dates_from_messages(messages_aggregator(162674267)))
# print('Possible age is', age_predict(141839173))
# 
