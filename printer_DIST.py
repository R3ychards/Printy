import os
import requests
import json
import time
import platform
import subprocess
from bs4 import BeautifulSoup
from PIL import Image
import PySimpleGUI as sg
import configparser
import ctypes
import sys
import operator
from shutil import copyfile

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# GUISETUP
layout = [[sg.Text("Inserisci l' indirizzo del tuo sito")],
          [sg.InputText()],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Inserisci il tuo link API', layout)

layout2 = [[sg.Text('Inserisci la tua chiave API')],
          [sg.InputText()],
          [sg.Submit(), sg.Cancel()]]

window2 = sg.Window('Inserisci la tua chiave api', layout2)

#Create config.ini file if not yet present
if os.path.isfile('config.ini') and os.path.isfile('PaperSettings.ini'):
    print("File already in path")
else:
    copyfile(resource_path('config.ini'), 'config.ini')
    copyfile(resource_path('PaperSettings.ini'), 'PaperSettings.ini')
    print('Wrote configs files.')

config = configparser.ConfigParser()
configpap = configparser.ConfigParser()
config.read('config.ini')
configpap.read('PaperSettings.ini')
api_link = config['API']['api_link']
First_run = config['API']['FirstRun']
lbnr= config['BlackList']['bllastnbr']
setupstep = config['API']['setupstep']
maxwidth = configpap['PaperSettings']['maxwidth']
fontsize = configpap['PaperSettings']['fontsize']
apikey = config['API']['api_key']
api = (api_link+"/api.php?key="+apikey)


if api_link != "":
    sg.popup("Api Key gia inserita")

if api_link == "":
    event, values = window.read()
    window.close()
    text_input = values[0]

    event2, values2 = window2.read()
    window2.close()
    key = values2[0]

    sg.popup('API inserita con successo', text_input)
    config.set('API', 'api_link', text_input)
    config.set('API', 'api_key', key)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
        time.sleep(0.4)
    api_link = config['API']['api_link']
    apikey = config['API']['api_key']
    api = (api_link + "/api.php?key=" + apikey)


if First_run == ("True"):
    process = ""
    if setupstep == "0":
        if is_admin():
            drvpth = resource_path("Application_Support\h58drv\h58drv.exe")
            sg.popup("Completa l' installazione del driver e riapri il programma")
            p = subprocess.Popen(drvpth, shell=True,
                                 stdout=subprocess.PIPE, universal_newlines=True)
            config.set('API', 'setupstep', "1")
            config.set('API', 'firstrun', "False")
            with open('config.ini','w') as configfile:
                config.write(configfile)
            time.sleep(0.6)
            sys.exit()
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
            time.sleep(0.6)
            sys.exit()


print("Connection to api..")
api_serve = requests.get(api)
print("Server_Response:" + str(api_serve.status_code))
rawdata = api_serve.json()
data = api_serve.text
parse_json = json.loads(data)
print("LEN Main_Array-->" + str(len(parse_json)) + " Ord. Fatti")
lenght = len(parse_json)
tgte = lenght - 1
print(tgte)
arleng = len(parse_json[tgte]['carrello'])
print(arleng)
adapt_range = range(arleng)
dataout = parse_json[0]['id_ordini']

items = list(range(lenght))
limit = lenght
for index, item in enumerate(items):
    dataout = parse_json[item]['id_ordini']
    parser_orario = parse_json[item]['oraconsegna']
    parser_t_o = parse_json[item]['tipo_ordine']
    parser_nc = parse_json[item]['note_consegna']
    parser_dconsegna = parse_json[item]['dataconsegna']
    parser_data = parse_json[item]['nome_prodotto_lavorazione']
    parser_oraacq = parse_json[item]['tempo_inizio_procedura_acquisto']
    parser_payment_method = parse_json[item]['pagamento']
    parser_tot_eur = parse_json[item]['totale']
    parser_name = (parse_json[item]['dati_utente'][0]['first_name'] + " " + parse_json[item]['dati_utente'][0][
        'last_name'])
    parser_addr = (parse_json[item]['dati_utente'][0]['indirizzo'] + " " + parse_json[item]['dati_utente'][0][
        'numero_civico'] + "\n" + parse_json[item]['dati_utente'][0]['citta']
                   + " " + parse_json[item]['dati_utente'][0]['cap'] + "\n" + parse_json[item]['dati_utente'][0][
                       'provincia']
                   )
    parser_tel = ("Tel: " + parse_json[item]['dati_utente'][0]['prefisso_int'] +
                  " " + parse_json[item]['dati_utente'][0]['telefono'])
    time.sleep(0.0)
    if index == limit:
        print("DATA PARSED SUCCESSFULLY")
        break

with open(resource_path('SampleOrder.htm')) as htm_file:
    soup = BeautifulSoup(htm_file.read(), features='html.parser')

    curnr=dataout

    tag = ""

    for tag_ora in soup.find_all(id='OS'):
        print(tag_ora.text)
        print(tag)
        if tag_ora.text == "Ora_Prep":
            print("Found & Replaced ORA Consegna")
            tag_ora.string = ("Preparazione " + str(parser_oraacq))

    for tag_ord in soup.find_all(id='ID_ORDINE'):
        print("found_order")
        print(tag_ord.text)
        print(tag)
        if tag_ord.text == "NR_ORD":
            print("Found & Replaced NR_ORD")
            tag_ord.string = dataout

    for tag_tipo in soup.find_all(id='Tipo_Ordine'):
        print("found_order")
        print(tag_tipo.text)
        print(tag)
        if tag_tipo.text == "Tipo_Ordine":
            print("Found & Replaced Tipo_Ordine")
            tag_tipo.string = parser_t_o

    for tag_nc in soup.find_all(id='noteconsegna'):
        print("found_nc")
        print(tag_nc.text)
        print(tag)
        if tag_nc.text == "noteconsegna":
            print("Found & Replaced Note_Consegna")
            print(parser_t_o)
            if parser_nc == "":
                tag_nc.string = ""
                print("Empty")
                print(parser_nc)
            else:
                print("full")
                print(parser_nc)
                tag_nc.string = parser_nc

    for tag_oc in soup.find_all(id='ora_cons'):
        print("found_order")
        print(tag_oc.text)
        print(tag)
        if tag_oc.text == "Consegna_Dati":
            print("Found & Replaced Consegna_Dati")
            tag_oc.string = ("Consegna ore " + str(parser_orario) + " del \n")

    for tag_tot in soup.find_all(id='totale_ordine'):
        print("found_order")
        print(tag_tot.text)
        print(tag)
        if tag_tot.text == "Tot_Ordine":
            print("Found & Replaced tag_tot")
            tag_tot.string = (str(parser_tot_eur))

    for tag_tp in soup.find_all(id='tipo_pagamento'):
        print("found_order")
        print(tag_tp.text)
        print(tag)
        if tag_tp.text == "Tipo_Pagamento":
            print("Found & Replaced tag_tp")
            tag_tp.string = (str(parser_payment_method))

    for tag_tp in soup.find_all(id='tipo_pagamento'):
        print("found_order")
        print(tag_tp.text)
        print(tag)
        if tag_tp.text == "Tipo_Pagamento":
            print("Found & Replaced tag_tp")
            tag_tp.string = (str(parser_payment_method))

    for tag_nln in soup.find_all(id='Nome_Cognome'):
        print("found_order")
        print(tag_nln.text)
        print(tag)
        if tag_nln.text == "Nome_Cognome":
            print("Found & Replaced tag_nln")
            tag_nln.string = (str(parser_name))

    for tag_addr in soup.find_all(id='address'):
        print("found_order")
        print(tag_addr.text)
        print(tag)
        if tag_addr.text == "dat_addr":
            print("Found & Replaced tag_addr")
            print(parser_addr)
            tag_addr.string = (str(parser_addr))

    for tag_tel in soup.find_all(id='tel'):
        print("found_order")
        print(tag_tel.text)
        print(tag)
        if tag_tel.text == "nr_tel":
            print("Found & Replaced tag_tel")
            tag_tel.string = (str(parser_tel))

    #Adding cust to body style in SampleOrder.htm
    for tag in soup.findAll(id="body"):
        tag['style'] = ("max-width: "+maxwidth+"mm; font-size: "+fontsize+"px ;")

    # Building needed arrays
    arr_tutti_i_dati = [None] * arleng
    arr_nome_prodotto = [None] * arleng
    arr_aggiungere = [None] * arleng
    arr_rimuovere = [None] * arleng
    arr_prodotto = [""] * arleng
    arr_qta = [0] * arleng

    # Cycle for initial data parse
    print("cycl-1")
    for index_dp, item_dp in enumerate(range(arleng)):
        arr_tutti_i_dati[item_dp] = parse_json[2]['carrello'][item_dp]['id_prodotto']
        print(str(item_dp) + "-->" + arr_tutti_i_dati[item_dp])

    # Second Cycle for Second array and third
    occurrences = {}
    for i in arr_tutti_i_dati:
        if i in occurrences:
            occurrences[i] += 1
        else:
            occurrences[i] = 1
    counter = 0
    for key, value in occurrences.items():
        arr_prodotto[counter] = key
        arr_qta[counter] = value
        counter = counter + 1

    # getting names
    lenghtfinalfor = len(occurrences)
    for index_tp, item_tp in enumerate(range(lenghtfinalfor)):
        isFound = False
        counterwhile01 = 0
        while isFound == False:
            if parse_json[2]['carrello'][counterwhile01]['id_prodotto'] == arr_prodotto[item_tp]:
                arr_nome_prodotto[item_tp] = parse_json[2]['carrello'][counterwhile01]['nome_prodotto']
                arr_aggiungere[item_tp] = parse_json[2]['carrello'][counterwhile01]['aggiungere']
                arr_rimuovere[item_tp] = parse_json[2]['carrello'][counterwhile01]['rimuovere']
                isFound = True
            print("AA")
            counterwhile01 = counterwhile01 + 1

    # Write to append
    print(len(occurrences))
    counter = 0
    div = soup.select_one("#links")
    for index_wo, item_wo in enumerate(range(lenghtfinalfor)):
        if arr_aggiungere[0] != "" and arr_rimuovere[0] != "":
            new_string_to_append = ("<br><strong>" + arr_nome_prodotto[counter] + "</strong> X <strong>" + str(
                arr_qta[counter]) + "</strong>"
                                    "<br>+" + arr_aggiungere[counter] +
                                    "<br>-" + arr_rimuovere[counter] +
                                    "<br>" + "--------------")
            div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
            print(div)
        if arr_aggiungere[0] == "" and arr_rimuovere[0] == "":
            new_string_to_append = ("<br><strong>" + arr_nome_prodotto[counter] + "</strong> X <strong>" + str(
                arr_qta[counter]) + "</strong>"
                                    "<br>" + "--------------")
            div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
        if arr_aggiungere[0] != "" and arr_rimuovere[0] == "":
            new_string_to_append = ("<br><strong>" + arr_nome_prodotto[counter] + "</strong> X <strong>" + str(
                arr_qta[counter]) + "</strong>"
                                    "<br>+" + arr_aggiungere[counter] +
                                    "<br>" + "--------------")
            div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
        if arr_aggiungere[0] == "" and arr_rimuovere[0] != "":
            new_string_to_append = ("<br><strong>" + arr_nome_prodotto[counter] + "</strong> X <strong>" + str(
                arr_qta[counter]) + "</strong>"
                                    "<br>-" + arr_rimuovere[counter] +
                                    "<br>" + "--------------")
            div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
        counter = counter + 1

    new_txt = soup.prettify()

with open('Order_Compiled.html', mode='w') as new_htm_file:
    print(soup)
    print("----")
    print(new_txt)
    new_htm_file.write(str(soup))
    time.sleep(4)
    print("Save Successful")

final_printout = (resource_path("Application_Support\p2p\p2p.exe")+" -print-to-default -print-settings ""noscale"" "+" printout.pdf")
wkcomm = (resource_path("Application_Support\wk\wkhtmltopdf.exe")+
          " --encoding utf-8 --margin-top 1mm --margin-bottom 7mm --margin-left 0mm --margin-right 0mm "
          +"Order_Compiled.html"+" printout.pdf")
pwktohtml = subprocess.Popen(wkcomm, shell=True,
                             stdout=subprocess.PIPE, universal_newlines=True)
time.sleep(3)
if (curnr > lbnr):
    printout_send = subprocess.Popen(final_printout, shell=True,
                                 stdout=subprocess.PIPE, universal_newlines=True)
    config.set('BlackList', 'bllastnbr', str(curnr))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    print("Already printed!")
    time.sleep(1.3)
    sys.exit()

