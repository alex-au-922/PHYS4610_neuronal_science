from plyer import notification
from slack_sdk import WebClient
import yaml
import os
def sendNotification(appName, message):
    # path to notification window icon
    ICON_PATH = os.path.join("utils", 'python_logo.png')
    
    notification.notify(title= appName,
                    message= message,
                    app_icon = ICON_PATH,
                    timeout= 1800,
                    toast=False)

def slack_message(message):
    try:
        with open('slackbotCredential.yaml') as stream:
            botConstant = yaml.safe_load(stream)
        token = botConstant['BOTTOKEN']
        sc = WebClient(token)

        sc.api_call('chat.postMessage',
        json = { 'channel': botConstant['CHANNEL'], 
                    'text': message})
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    sendNotification('Testing','Finish Run')
