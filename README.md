# smart_agricolture_IoT_project

## TODO

* [x] inserire supporto per mysqldb in command.py
* [x] inserire supporto per mysqldb in from_node.py
* [x] spostare tutte le operazioni su mysql su un file
* [x] scrivere controlli di buona riuscita delle funzioni del modulo mysql
* [x] scrivere le funzioni e comandi per modificare land e config di default
* [x] mettere il limit alle funzioni get
* [x] testare funzionalità server
* [x] scrivere un log module che scrive sia su file sia su terminale

* [x] usare una lista per bufferizzare i messaggi da inviare in mqtt
* [x] inserire mqtt nel nodo e testarlo
* [x] aggingere il campo protocol (COAP/MQTT) alle config in sql
* [x] testare server
* [x] inserire mqtt nel server (modificare json)
* [x] testare configurazione del nodo e occuparmi dei TODO 
* [x] capire pwerchè il while di configurazione non funziona
* [x] far tornare al reset il nodo se la land non esiste
* [x] test di tutti i comandi

### NODO MQTT

* [ ] cercare di dividere il file mqtt-node.c in più file (tutti in una cartella)
* [ ] togliere il log
* [ ] controllare se tutte le librerie servono

### NODO COAP

* [x] capire problema con la funzione COAP_BLOCKING_REQUEST
* [x] ridfinizione protocolli coap
* [x] controllare i protocolli negli handler delle risorse
* [x] inserire i trigger delle risorse nei posti corretti
* [x] scrivere le funzioni da client coap
* [x] adattare il processo
* [x] eliminare i rimasugli del modulo mqtt
* [x] fare attenzione ai problemi di visibilità delle funzioni
* [ ] controllare se tutte le librerie servono
* [x] capire perchè all'assign config fa crashare il nodo su cooja

### COAP SERVER
* [x] inserire COAP nel server
* [ ] vedere se i file.h sono aggiornati con tutte le funzioni
* [x] capire perchè con cooja non ricevo nulla (vedere il border router!)
* [x] capire perchè l'observing lato server da delle eccezioni
* [ ] capire perchè non invia il payload con il put
* [ ] capire come contattare i nodi all'avvio se questi sono già configurati


