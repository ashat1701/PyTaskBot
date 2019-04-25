import database
import google.oauth2.credentials
import googleapiclient.discovery
import datetime


def get_today_tasks_list(chat_id):
    db = database.Database()
    creds_dict = db.get_cred(chat_id)
    del creds_dict["chat_id"]
    print(creds_dict)
    credentials = google.oauth2.credentials.Credentials(**creds_dict)
    calendar = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    # TODO: fix this for other UTC
    today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    start_of_day = today.isoformat() + '+03:00'
    end = datetime.datetime.combine(datetime.date.today(), datetime.datetime.max.time())
    end_of_day = end.isoformat() + '+03:00'
    print(start_of_day, end_of_day)
    events_result = calendar.events().list(calendarId="primary", singleEvents=True, orderBy='startTime', timeMin=start_of_day, timeMax=end_of_day).execute()
    events = events_result.get('items', [])
    if not events:
        return "No today events"
    else:
        return events
