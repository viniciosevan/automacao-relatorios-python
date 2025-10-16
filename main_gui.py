import PySimpleGUI as sg
import datetime


layout = [
    [sg.Text("Horário de envio (HH:MM):"), sg.InputText("18:00", key="hora")],
    [sg.Text("Destinatários (separados por vírgula):"), sg.InputText("email@empresa.com", key="emails")],
    [sg.Button("Salvar Configurações"), sg.Button("Enviar Agora")],
    [sg.Output(size=(60, 10))] 
]

window = sg.Window("Sistema de Relatórios", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  
        break
    elif event == "Salvar Configurações":
        print(f"Configurações salvas: Hora = {values['hora']}, Emails = {values['emails']}")
        
    elif event == "Enviar Agora":
        print("Enviando relatório manualmente...")
        

window.close()  
