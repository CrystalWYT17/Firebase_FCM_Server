import firebase_admin
from firebase_admin import credentials, messaging

credential = credentials.Certificate("wbgt_firestore.json")
firebase_admin.initialize_app(credential)

def sendNotification(registrationToken, dataObject=None):
    message = messaging.MulticastMessage(tokens= registrationToken,
                                         data=dataObject)
    
    response = messaging.send_multicast(message)
    print("response code: ", response)
    