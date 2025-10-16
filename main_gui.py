import PySimpleGUI as sg
import datetime

# Use sg.Text em vez de PySimpleGUI.Text
layout = [
    [sg.Text("Horário de envio (HH:MM):"), sg.InputText("18:00", key="hora")],
    [sg.Text("Destinatários (separados por vírgula):"), sg.InputText("email@empresa.com", key="emails")],
    [sg.Button("Salvar Configurações"), sg.Button("Enviar Agora")],
    [sg.Output(size=(60, 10))]  # Área para mostrar logs/status
]

window = sg.Window("Sistema de Relatórios", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # Correção: use sg.WIN_CLOSED em vez de sg.WINDOW_CLOSED
        break
    elif event == "Salvar Configurações":
        print(f"Configurações salvas: Hora = {values['hora']}, Emails = {values['emails']}")
        # Aqui você pode salvar essas configurações em um arquivo config.json
    elif event == "Enviar Agora":
        print("Enviando relatório manualmente...")
        # Aqui você chama sua função gerar_relatorio() passando os valores do GUI

window.close()  # Não esqueça de fechar a janela ao final