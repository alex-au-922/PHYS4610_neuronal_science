from plyer import notification
import os
def sendNotification(appName, message):
    # path to notification window icon
    ICON_PATH = os.path.join("utils", 'python_logo.png')
    
    notification.notify(title= appName,
                    message= message,
                    app_icon = ICON_PATH,
                    timeout= 1800,
                    toast=False)
if __name__ == '__main__':
    sendNotification('Testing','Finish Run')
