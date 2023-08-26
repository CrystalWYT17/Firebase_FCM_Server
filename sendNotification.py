import fcmAdmin
from firebase_admin import firestore
import sched, time
import allstations

#reference to firestore database
db = firestore.client()

all_tokens = []
def getAllTokens():
    collection_name = "users"
    collection_ref = db.collection(collection_name)

    document = collection_ref.stream()
    #get_all
    for doc in document:
        token = doc.to_dict().get("token")
        all_tokens.append(token)

    print(all_tokens)
    
def sendNotification(extra_data):
    fcmAdmin.sendNotification(all_tokens, extra_data)

def sendBroadcast():
    all_stations_wbgt = {}
    getAllTokens()
    #get wbgt of all stations
    all_stations_wbgt = allstations.predict_wbgt()
    for station, wbgt in all_stations_wbgt.items():
        #print(station, wbgt)
        if(wbgt >= 30):
            print("stationId : "+station)
            title = "Heat Stress Warning"
            body = station+" predicted wbgt value of "+ str(wbgt)
            extra_data = {"station_id": station,
                          "title": title,
                          "body": body}
            sendNotification(extra_data=extra_data)
            extra_data.clear()

    all_tokens.clear()

#sendBroadcast()

intervalSeconds = 180
def runEvery3Mins(schedular, interval):
    sendBroadcast()
    print("done.....")
    schedular.enter(interval, 1, runEvery3Mins, (schedular, interval))


schedular = sched.scheduler(time.time, time.sleep)
schedular.enter(0, 1, runEvery3Mins, (schedular, intervalSeconds))
schedular.run()