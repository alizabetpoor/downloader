from threading import Thread
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED

from socket import AF_INET, SOCK_STREAM, socket

layout=[
        [sg.Text("file location: "),sg.Input(key="-FILE-",size=(30,2)),sg.FileBrowse(size=(20,1))],
        [sg.Text("ip reciever:"),sg.InputText(key="-IP-")],
        [sg.Text("port reciever:"),sg.InputText(key="-PORT-")],
        [sg.Button("send",key="send-btn",size=(8,2))],
        [sg.ProgressBar(2,orientation="h",size=(20,15),key="-progress-bar-",bar_color=("green","white"))],
]

window=sg.Window("sender app",layout=layout,size=(500,200),font="Arial 12",element_justification="c")



def send_file(file,ip,port):
    with open(file=file,mode="rb") as file:
        data=file.read()
    try:
        sock=socket(AF_INET,SOCK_STREAM)
        sock.connect((ip,port))

        bar=int(len(data)/1024)
        i=0
        window["-progress-bar-"].UpdateBar(0,bar)
        while True:
            if len(data)>0:
                tmp_data=data[0:1024]
                if len(tmp_data)<1024:
                    tmp_data+=chr(0).encode()*(1024-len(tmp_data))
                data=data[1024:]
                sock.send(tmp_data)
                i+=1
                window["-progress-bar-"].UpdateBar(i)  
            else:
                # sock.send(file.encode())
                sock.close()
                break
        window.write_event_value("-end-task-","file sended")
    except:
        window.write_event_value("-error-","error happened")

thread=None

while True:
    event,inputstr=window.read()
    if event==sg.WINDOW_CLOSED:
        break
    elif event=="send-btn" and not thread and inputstr["-PORT-"].isdigit() and \
        not inputstr["-IP-"].isalnum():
        window["-progress-bar-"].UpdateBar(0)
        file=inputstr["-FILE-"]
        ip=inputstr["-IP-"]
        port=int(inputstr["-PORT-"])
        thread=Thread(target=send_file,args=(file,ip,port))
        thread.start()
    elif event=="-error-":
        thread=None
        sg.PopupAutoClose("check you ip or port",title="error")
    elif event=='-end-task-':
        thread=None
        sg.popup("the file has been sent")
window.close()