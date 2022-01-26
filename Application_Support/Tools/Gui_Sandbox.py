import PySimpleGUI as sg      

layout = [[sg.Text('Inserisci il tuo link API')],      
                 [sg.InputText()],      
                 [sg.Submit(), sg.Cancel()]]      

window = sg.Window('Inserisci il tuo link API', layout)    

event, values = window.read()    
window.close()

text_input = values[0]
print("Val="+values[0])
sg.popup('API inserita con successo')