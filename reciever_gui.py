from threading import Thread
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import No, WIN_CLOSED
from socket import AF_INET, SOCK_STREAM, socket


def recieve_data(ip,port):
    global thread
    filedata=b""
    try:
        sock=socket(AF_INET,SOCK_STREAM)
        sock.bind((ip,port))
        sock.listen()
        sender,addr=sock.accept()
        while True:
            data=sender.recv(1024)
            if len(data)==0:
                sock.close()
                
                break
                        
                
                
                
            filedata+=data
        window.write_event_value("-end-task-",filedata)
    except:
        window.write_event_value("-problem-","problem happened")
        

layout=[
        [sg.Text("your ip:"),sg.InputText(key="-IP-")],
        [sg.Text("your port:"),sg.InputText(key="-PORT-")],
        [sg.Button("start recieving",key="-btn-recieve-",border_width=2,s=(11,2),pad=(0,15))],
        
]

window=sg.Window("recieve app",layout=layout,font="Arial 12",element_justification="c",size=(400,150))



thread=None
while True:
    event,inputstr=window.read()
    
    if event==sg.WIN_CLOSED:
        break
    elif event=="-btn-recieve-" and not thread and inputstr["-PORT-"].isdigit() and \
        not inputstr["-IP-"].isalnum():
        ip=inputstr["-IP-"]
        port=int(inputstr["-PORT-"])
        
        thread=Thread(target=recieve_data,args=(ip,port),daemon=True)
        thread.start()
        sg.popup_auto_close("waiting for sender...",auto_close_duration=2)
    elif event=="-problem-":
        thread=None
        sg.popup_no_titlebar("correct your ip or port")
    elif event=="-end-task-":
        data_file=inputstr[event]
        thread=None
        text=sg.popup_get_text("name of the file:","save file")
        with open(text,"wb") as file:
            file.write(data_file)
            sg.popup("file has been saved")
       

window.close()