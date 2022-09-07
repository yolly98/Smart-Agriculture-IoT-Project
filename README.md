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

### NODO COAP

* [ ] ridfinizione protocolli coap
* [ ] controllare i protocolli negli handler delle risorse
* [ ] inserire i trigger delle risorse nei posti corretti
* [ ] scrivere le funzioni da client coap
* [ ] adattare il processo

### COAP SERVER
* [ ] inserire COAP nel server
* [ ] vedere se i file.h sono aggiornati con tutte le funzioni
* [ ] capire perchè con cooja non ricevo nulla (vedere il border router!)
