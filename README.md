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
* [x] risolvere problema del messaggio troppo lungo per assign_config
* [ ] risolvere problema doppioni sulla rete

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
* [x] gestire caso land non trovata

### COAP SERVER
* [x] inserire COAP nel server
* [ ] vedere se i file.h sono aggiornati con tutte le funzioni
* [x] capire perchè con cooja non ricevo nulla (vedere il border router!)
* [x] capire perchè l'observing lato server da delle eccezioni
* [x] capire perchè non invia il payload con il put e get (funzionano solo richieste vuote)
* [x] capire come contattare i nodi all'avvio se questi sono già configurati
* [x] risolvere tutti i problemi di configurazione (server si avvia quando già il nodo è attivo e configurato)
* [x] capire perchè non riesco a mandare comandi (es. semplice get sensor)
* [x] capire perchè ricevo duplicati alla lettura sensori
* [x] capire perchè a volte assegna configurazione a 0
* [x] capire perchè il timer non viene resettato quando lo modifico
* [x] capire perchè a volte il server non riceve
* [x] Se è attivo il nodo e il server si attiva dopo, poi non posso fargli l'osserving
* [x] perchè quando invio un comando ricevo dall'observing?
* [x] gestire caso land non trovata
* [x] test offline dopo timer e is_alive
* [x] mettere controllo nodi già configurati per evitare doppioni sulla rete
* [x] se mi connetto ad una rete già configurata in alcuni casi ho ancora l'errore 'TooManyObserver'

* [x] fare test con 4 nodi coap
* [ ] rifare test mqtt (cooja)
* [ ] fare test con 4 nodi mqtt
* [ ] fare test con 2 nodi coap e 2 mqtt
* [ ] vedere se process_exit(&mqtt_node) funztiona nel mqtt_node (se no sostituire con PROCESS_EXIT())



