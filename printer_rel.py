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
layout = [[sg.Text("Inserisci la url del tuo sottodominio (es: https://nome.dominio.it/)")],
          [sg.InputText()],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Inserisci il tuo link API', layout)

layout2 = [[sg.Text('Inserisci la tua chiave API, nel tuo pannello di controllo, nella sezione Configurazione->API')],
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

if os.path.isfile('orders.json'):
    ("JSON Already in Path")
else:
    copyfile(resource_path('orders.json'), 'orders.json')
    print("Wrote JSON file")


config = configparser.ConfigParser()
configpap = configparser.ConfigParser()
config.read('config.ini')
configpap.read('PaperSettings.ini')
api_link = config['API']['api_link']
First_run = config['API']['FirstRun']
setupstep = config['API']['setupstep']
maxwidth = configpap['PaperSettings']['maxwidth']
fontsize = configpap['PaperSettings']['fontsize']
apikey = config['API']['api_key']
api = (api_link+"api.php?key="+apikey)

if api_link != "":
    sg.popup("Api Key gia inserita")

if api_link == "":
    event, values = window.read()
    window.close()
    text_input = values[0]

    sg.popup('Sito inserito con successo', text_input)

    event2, values2 = window2.read()
    window2.close()
    key = values2[0]

    sg.popup('API key con successo', text_input)
    config.set('API', 'api_link', text_input)
    config.set('API', 'api_key', key)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
        #time.sleep(0.4)
    api_link = config['API']['api_link']
    apikey = config['API']['api_key']
    api = (api_link + "api.php?key=" + apikey)
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
            #time.sleep(0.6)
            sys.exit()
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
            #time.sleep(0.6)
            sys.exit()

#Main cycle, with time
looper=0
while looper==0:
    parse_json="";
    print("Connection to api..")
    api_serve = requests.get(api)
    print("Server_Response:" + str(api_serve.status_code))
    rawdata = api_serve.json()
    data = api_serve.text
    parse_json = json.loads(data)
    print("LEN Main_Array-->" + str(len(parse_json)) + " Ord. Fatti")
    last_done = config['BlackList']['bllastnbr']

    
    
    

    lenght = len(parse_json)
    tgte = lenght -1 #Lunghezza tutti i dati


    if tgte < 0:
        print("Nessun ordine presente, attendo")
    if tgte >= 0 and tgte <= int(last_done):
        print("Ordine gia stampato, attendo nuovi ordini")
    if tgte >= 0:
        arleng = len(parse_json[tgte]['carrello'])
        print(arleng)
        adapt_range = range(arleng)
        for index_par, item_par in enumerate(range(lenght)):
            curr_id= parse_json[item_par]['id_ordini']
            with open('orders.json') as file:
                tot_orders = json.loads(file.read())
                
            #time.sleep(2)

            
            if(len(tot_orders["ordini"]) != 0):
                print("Current ID:",str(curr_id))
                checkExist = False
                for item in tot_orders["ordini"]:
                    if(curr_id == item):
                        checkExist = True

                if(checkExist == True):
                    print("Already done")
                    #Non fa nulla
                else:
                    #Inserisci nel json
                    if int(curr_id) <= int(last_done):
                            print("Already done")
                    if (int(last_done)+1) != int(curr_id) and int(last_done) != int(curr_id):
                        sub_factor=int(last_done)-int(curr_id)
                        print("SubFactor="+str(sub_factor))
                        todo=int(curr_id)-sub_factor
                        for indexfo,itemfo in enumerate(range(lenght)):
                            if parse_json[indexfo]['id_ordini'] == str(todo):
                                print("Found nr back")
                                item_par=itemfo
                    if int(curr_id) > int(last_done):
                        cart_len = len(parse_json[item_par]['carrello'])
                        dataout = parse_json[item_par]['id_ordini']
                        parser_orario = parse_json[item_par]['oraconsegna']
                        parser_t_o = parse_json[item_par]['tipo_ordine']
                        parser_nc = parse_json[item_par]['note_consegna']
                        parser_dconsegna = parse_json[item_par]['dataconsegna']
                        parser_data = parse_json[item_par]['nome_prodotto_lavorazione']
                        parser_oraacq = parse_json[item_par]['tempo_inizio_procedura_acquisto']
                        parser_payment_method = parse_json[item_par]['pagamento']
                        parser_zona = parse_json[item_par]['zona']
                        parser_tot_eur = parse_json[item_par]['totale']
                        if parse_json[item_par]['dati_utente'][0]['indirizzo'] == None:
                            parsed_addr = ""
                        if parse_json[item_par]['dati_utente'][0]['indirizzo'] != None:
                            parsed_addr = parse_json[item_par]['dati_utente'][0]['indirizzo']
                        if parse_json[item_par]['dati_utente'][0]['numero_civico'] == None:
                            parsed_cv = ""
                        if parse_json[item_par]['dati_utente'][0]['numero_civico'] != None:
                            parsed_cv = parse_json[item_par]['dati_utente'][0]['numero_civico']
                        if  parse_json[item_par]['dati_utente'][0]['citta'] != None:
                            parsed_citta =  parse_json[item_par]['dati_utente'][0]['citta']
                        if  parse_json[item_par]['dati_utente'][0]['citta'] == None:
                            parsed_citta =" "
                        if parse_json[item_par]['dati_utente'][0]['cap'] == None:
                            parsed_cap= ""
                        if parse_json[item_par]['dati_utente'][0]['cap'] != None:
                            parsed_cap= parse_json[item_par]['dati_utente'][0]['cap']
                        if parse_json[item_par]['dati_utente'][0]['provincia'] != None:
                            parsed_prov= parse_json[item_par]['dati_utente'][0]['provincia']
                        if parse_json[item_par]['dati_utente'][0]['provincia'] == None:
                            parsed_prov = ""
                        parser_name = (
                                    parse_json[item_par]['dati_utente'][0]['first_name'] + " " + parse_json[item_par]['dati_utente'][0][
                                'last_name'])
                        parser_addr = (
                                    parsed_addr + " " + parsed_cv + "\n" + parsed_citta
                                    + " " + parsed_cap + "\n" + parsed_prov
                                    )
                        parser_tel = ("Tel: " + parse_json[item_par]['dati_utente'][0]['prefisso_int'] +
                                    " " + parse_json[item_par]['dati_utente'][0]['telefono'])
                        #time.sleep(0.0)
                        print("Data parsed successfully")

                        with open(resource_path('SampleOrder.htm')) as htm_file:
                            soup = BeautifulSoup(htm_file.read(), features='html.parser')

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
                                    tag_oc.string = ("Consegna ore " + str(parser_orario) + " del \n"+str(parser_dconsegna))

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

                            if parser_zona != 0:
                                for tag_zone in soup.find_all(id='zone'):
                                    print("found_order")
                                    print(tag_zone.text)
                                    print(tag)
                                    if tag_zone.text == "":
                                        print("Found & Replaced Zone")
                                        tag_zone.string = (str(parser_payment_method))

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

                            # Adding cust to body style in SampleOrder.htm
                            for tag in soup.findAll(id="body"):
                                tag['style'] = ("max-width: " + maxwidth + "mm; font-size: " + fontsize + "px ;")

                                # Building needed arrays
                            arr_tutti_i_dati = [""] * cart_len
                            arr_nome_prodotto = [""] * cart_len
                            arr_aggiungere = [""] * cart_len
                            arr_rimuovere = [""] * cart_len
                            arr_prodotto = [""] * cart_len
                            arr_qta = [0] * cart_len

                            # Cycle for first data load
                            print("cycl-1")
                            print(cart_len)
                            print("AAA!")
                            print("CartLeng+"+str(cart_len))
                            for index_dp, item_dp in enumerate(range(cart_len)):
                                arr_tutti_i_dati[item_dp] = parse_json[item_par]['carrello'][item_dp]['id_prodotto']
                                print(str(item_dp) + "-->" + arr_tutti_i_dati[item_dp])

                            # Second Cycle for Second array and third
                            occurrences = {}

                            for i in arr_tutti_i_dati:
                                if i in occurrences:
                                    occurrences[i] += 1
                                else:
                                    occurrences[i] = 1

                            counter = 0
                            
                            print("for key, value in occurrences.items()")
                            for key, value in occurrences.items():
                                print(key)
                                print(value)
                                arr_prodotto[counter] = key
                                arr_qta[counter] = value
                                counter = counter + 1

                            # getting names/things to add/remove
                            counter=0


                            print("arr_prodotto:", str(arr_prodotto))
                            
                            #! FIX ERRORE
                            for index_tp, item_tp in enumerate(range(cart_len)):

                                for item, i in enumerate(range(len(arr_prodotto))):
                                    print(parse_json[item_par]['carrello'][item_tp]['id_prodotto'],"->",arr_prodotto[i])
                                    
                                    if parse_json[item_par]['carrello'][item_tp]['id_prodotto'] == arr_prodotto[i]:
                                        print(parse_json[item_par]['carrello'][item_tp]['nome_prodotto'])
                                        arr_nome_prodotto[i] = parse_json[item_par]['carrello'][item_tp]['nome_prodotto']
                                        arr_aggiungere[i] = parse_json[item_par]['carrello'][item_tp]['aggiungere']
                                        arr_rimuovere[i] = parse_json[item_par]['carrello'][item_tp]['rimuovere']
                                
                            #! FIX ERRORE      

                            counter = 0
                            div = soup.select_one("#links")
                            for index_wo, item_wo in enumerate(range(cart_len)):
                                if arr_aggiungere[item_wo] != "" and arr_rimuovere[item_wo] != "" and arr_prodotto[item_wo] != "":
                                    new_string_to_append = ("<br><strong>" + arr_nome_prodotto[
                                        counter] + "</strong> X <strong>" + str(
                                        arr_qta[counter]) + "</strong>"
                                                                    "<br>+" + arr_aggiungere[counter] +
                                                                    "<br>-" + arr_rimuovere[counter] +
                                                                    "<br>" + "--------------")
                                    div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
                                if arr_aggiungere[item_wo] == "" and arr_rimuovere[item_wo] == "" and arr_prodotto[item_wo] != "":
                                    new_string_to_append = ("<br><strong>" + arr_nome_prodotto[
                                                counter] + "</strong> X <strong>" + str(
                                                arr_qta[counter]) + "</strong>"
                                                                    "<br>" + "--------------")
                                    div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
                                if arr_aggiungere[item_wo] != "" and arr_rimuovere[item_wo] == "" and arr_prodotto[item_wo] != "":
                                    new_string_to_append = ("<br><strong>" + arr_nome_prodotto[
                                                counter] + "</strong> X <strong>" + str(
                                                arr_qta[counter]) + "</strong>"
                                                                    "<br>+" + arr_aggiungere[counter] +
                                                                    "<br>" + "--------------")
                                    div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
                                if arr_aggiungere[item_wo] == "" and arr_rimuovere[item_wo] != "" and arr_prodotto[item_wo] != "":
                                    new_string_to_append = ("<br><strong>" + arr_nome_prodotto[
                                                counter] + "</strong> X <strong>" + str(
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
                                #time.sleep(4)
                                print("Save Successful")

                            final_printout = (resource_path(
                                        "Application_Support\p2p\p2p.exe") + " -print-to-default -print-settings ""noscale"" " + " printout.pdf")
                            wkcomm = (resource_path("Application_Support\wk\w2pdf.exe") +
                                            " --encoding utf-8 --margin-top 1mm --margin-bottom 7mm --margin-left 0mm --margin-right 0mm "
                                            + "Order_Compiled.html" + " printout.pdf")
                            pwktohtml = subprocess.Popen(wkcomm, shell=True,
                                                                stdout=subprocess.PIPE, universal_newlines=True)
                            #time.sleep(30)
                            time.sleep(4)
                            printout_send = subprocess.Popen(final_printout, shell=True,
                                                                    stdout=subprocess.PIPE, universal_newlines=True)
                            config.set('BlackList', 'bllastnbr', str(curr_id))

                            tot_orders["ordini"].append(curr_id)
                    
                            with open("orders.json", "w") as file:
                                json.dump(tot_orders, file)

                            api_print = (api_link+"apistampa.php?idordine="+curr_id+"&key="+apikey)
                            send_print = requests.get(api_print)
                            with open('config.ini', 'w') as configfile:
                                config.write(configfile)
                                print("File Saved, ID:", curr_id)
                    
            else:
                if int(curr_id) <= int(last_done):
                        print("Already done")
                if (int(last_done)+1) != int(curr_id) and int(last_done) != int(curr_id):
                    sub_factor=int(last_done)-int(curr_id)
                    print("SubFactor="+str(sub_factor))
                    todo=int(curr_id)-sub_factor
                    for indexfo,itemfo in enumerate(range(lenght)):
                        if parse_json[indexfo]['id_ordini'] == str(todo):
                            print("Found nr back")
                            item_par=itemfo
                if int(curr_id) > int(last_done):
                    cart_len = len(parse_json[item_par]['carrello'])
                    dataout = parse_json[item_par]['id_ordini']
                    parser_orario = parse_json[item_par]['oraconsegna']
                    parser_t_o = parse_json[item_par]['tipo_ordine']
                    parser_nc = parse_json[item_par]['note_consegna']
                    parser_dconsegna = parse_json[item_par]['dataconsegna']
                    parser_data = parse_json[item_par]['nome_prodotto_lavorazione']
                    parser_zona = parse_json[item_par]['zona']
                    parser_oraacq = parse_json[item_par]['tempo_inizio_procedura_acquisto']
                    parser_payment_method = parse_json[item_par]['pagamento']
                    parser_tot_eur = parse_json[item_par]['totale']
                    if parse_json[item_par]['dati_utente'][0]['indirizzo'] == None:
                        parsed_addr = ""
                    if parse_json[item_par]['dati_utente'][0]['indirizzo'] != None:
                        parsed_addr = parse_json[item_par]['dati_utente'][0]['indirizzo']
                    if parse_json[item_par]['dati_utente'][0]['numero_civico'] == None:
                        parsed_cv = ""
                    if parse_json[item_par]['dati_utente'][0]['numero_civico'] != None:
                        parsed_cv = parse_json[item_par]['dati_utente'][0]['numero_civico']
                    if  parse_json[item_par]['dati_utente'][0]['citta'] != None:
                        parsed_citta =  parse_json[item_par]['dati_utente'][0]['citta']
                    if  parse_json[item_par]['dati_utente'][0]['citta'] == None:
                        parsed_citta =" "
                    if parse_json[item_par]['dati_utente'][0]['cap'] == None:
                        parsed_cap= ""
                    if parse_json[item_par]['dati_utente'][0]['cap'] != None:
                        parsed_cap= parse_json[item_par]['dati_utente'][0]['cap']
                    if parse_json[item_par]['dati_utente'][0]['provincia'] != None:
                        parsed_prov= parse_json[item_par]['dati_utente'][0]['provincia']
                    if parse_json[item_par]['dati_utente'][0]['provincia'] == None:
                        parsed_prov = ""
                    parser_name = (
                                parse_json[item_par]['dati_utente'][0]['first_name'] + " " + parse_json[item_par]['dati_utente'][0][
                            'last_name'])
                    parser_addr = (
                                parsed_addr + " " + parsed_cv + "\n" + parsed_citta
                                + " " + parsed_cap + "\n" + parsed_prov
                                )
                    parser_tel = ("Tel: " + parse_json[item_par]['dati_utente'][0]['prefisso_int'] +
                                " " + parse_json[item_par]['dati_utente'][0]['telefono'])
                    #time.sleep(0.0)
                    print("Data parsed successfully")

                    with open(resource_path('SampleOrder.htm')) as htm_file:
                        soup = BeautifulSoup(htm_file.read(), features='html.parser')

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
                                tag_oc.string = ("Consegna ore " + str(parser_orario) + " del \n"+str(parser_dconsegna))

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

                        if parser_zona != 0:
                            for tag_zone in soup.find_all(id='zone'):
                                print("found_order")
                                print(tag_zone.text)
                                print(tag)
                                if tag_zone.text == "":
                                    print("Found & Replaced Zone")
                                    tag_zone.string = (str(parser_payment_method))

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

                        # Adding cust to body style in SampleOrder.htm
                        for tag in soup.findAll(id="body"):
                            tag['style'] = ("max-width: " + maxwidth + "mm; font-size: " + fontsize + "px ;")

                            # Building needed arrays
                        arr_tutti_i_dati = [""] * cart_len
                        arr_nome_prodotto = [""] * cart_len
                        arr_aggiungere = [""] * cart_len
                        arr_rimuovere = [""] * cart_len
                        arr_prodotto = [""] * cart_len
                        arr_qta = [0] * cart_len

                        # Cycle for first data load
                        print("cycl-1")
                        print(cart_len)
                        print("AAA!")
                        print("CartLeng+"+str(cart_len))
                        for index_dp, item_dp in enumerate(range(cart_len)):
                            arr_tutti_i_dati[item_dp] = parse_json[item_par]['carrello'][item_dp]['id_prodotto']
                            print(str(item_dp) + "-->" + arr_tutti_i_dati[item_dp])

                        # Second Cycle for Second array and third
                        occurrences = {}

                        for i in arr_tutti_i_dati:
                            if i in occurrences:
                                occurrences[i] += 1
                            else:
                                occurrences[i] = 1

                        counter = 0
                        
                        print("for key, value in occurrences.items()")
                        for key, value in occurrences.items():
                            print(key)
                            print(value)
                            arr_prodotto[counter] = key
                            arr_qta[counter] = value
                            counter = counter + 1

                        # getting names/things to add/remove
                        counter=0


                        print("arr_prodotto:", str(arr_prodotto))
                        
                        #! FIX ERRORE
                        for index_tp, item_tp in enumerate(range(cart_len)):

                            for item, i in enumerate(range(len(arr_prodotto))):
                                print(parse_json[item_par]['carrello'][item_tp]['id_prodotto'],"->",arr_prodotto[i])
                                
                                if parse_json[item_par]['carrello'][item_tp]['id_prodotto'] == arr_prodotto[i]:
                                    print(parse_json[item_par]['carrello'][item_tp]['nome_prodotto'])
                                    arr_nome_prodotto[i] = parse_json[item_par]['carrello'][item_tp]['nome_prodotto']
                                    arr_aggiungere[i] = parse_json[item_par]['carrello'][item_tp]['aggiungere']
                                    arr_rimuovere[i] = parse_json[item_par]['carrello'][item_tp]['rimuovere']
                            
                        #! FIX ERRORE      

                        counter = 0
                        div = soup.select_one("#links")
                        for index_wo, item_wo in enumerate(range(cart_len)):
                            if arr_aggiungere[item_wo] != "" and arr_rimuovere[item_wo] != "" and arr_prodotto[item_wo] != "":
                                new_string_to_append = ("<br><strong>" + arr_nome_prodotto[
                                    counter] + "</strong> X <strong>" + str(
                                    arr_qta[counter]) + "</strong>"
                                                                "<br>+" + arr_aggiungere[counter] +
                                                                "<br>-" + arr_rimuovere[counter] +
                                                                "<br>" + "--------------")
                                div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
                            if arr_aggiungere[item_wo] == "" and arr_rimuovere[item_wo] == "" and arr_prodotto[item_wo] != "":
                                new_string_to_append = ("<br><strong>" + arr_nome_prodotto[
                                            counter] + "</strong> X <strong>" + str(
                                            arr_qta[counter]) + "</strong>"
                                                                "<br>" + "--------------")
                                div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
                            if arr_aggiungere[item_wo] != "" and arr_rimuovere[item_wo] == "" and arr_prodotto[item_wo] != "":
                                new_string_to_append = ("<br><strong>" + arr_nome_prodotto[
                                            counter] + "</strong> X <strong>" + str(
                                            arr_qta[counter]) + "</strong>"
                                                                "<br>+" + arr_aggiungere[counter] +
                                                                "<br>" + "--------------")
                                div.append(BeautifulSoup(new_string_to_append, 'html.parser'))
                            if arr_aggiungere[item_wo] == "" and arr_rimuovere[item_wo] != "" and arr_prodotto[item_wo] != "":
                                new_string_to_append = ("<br><strong>" + arr_nome_prodotto[
                                            counter] + "</strong> X <strong>" + str(
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
                            #time.sleep(4)
                            print("Save Successful")

                        final_printout = (resource_path(
                                    "Application_Support\p2p\p2p.exe") + " -print-to-default -print-settings ""noscale"" " + " printout.pdf")
                        wkcomm = (resource_path("Application_Support\wk\w2pdf.exe") +
                                        " --encoding utf-8 --margin-top 1mm --margin-bottom 7mm --margin-left 0mm --margin-right 0mm "
                                        + "Order_Compiled.html" + " printout.pdf")
                        pwktohtml = subprocess.Popen(wkcomm, shell=True,
                                                            stdout=subprocess.PIPE, universal_newlines=True)
                        #time.sleep(30)
                        time.sleep(4)
                        printout_send = subprocess.Popen(final_printout, shell=True,
                                                                stdout=subprocess.PIPE, universal_newlines=True)
                        config.set('BlackList', 'bllastnbr', str(curr_id))

                        tot_orders["ordini"].append(curr_id)
                
                        with open("orders.json", "w") as file:
                            json.dump(tot_orders, file)

                        api_print = (api_link+"apistampa.php?idordine="+curr_id+"&key="+apikey)
                        send_print = requests.get(api_print)
                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                            print("File Saved, ID:", curr_id)
            
    time_to_sleep = 90

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * time_to_sleep))
    sys.stdout.flush()
    sys.stdout.write("\b" * (time_to_sleep+1)) # return to start of line, after '['

    for i in range(time_to_sleep):
        time.sleep(1) # do real work here
        # update the bar
        sys.stdout.write("=")
        sys.stdout.flush()

    sys.stdout.write("]\n") # this ends the progress bar

    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)