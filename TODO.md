# smart_agricolture_IoT_project

## TODO


### NODO MQTT

* [x] cercare di dividere il file mqtt-node.c in più file (tutti in una cartella)
* [ ] togliere il log
* [ ] controllare se tutte le librerie servono
* [x] risolvere problema del messaggio troppo lungo per assign_config
* [x] risolvere problema doppioni sulla rete
* [x] eliminare funzioni di simulazione (tranne la configurazione)
* [x] vedere se process_exit(&mqtt_node) funztiona nel mqtt_node (se no sostituire con PROCESS_EXIT())
* [x] spezzare l'invio della configurazione in due pezzi(altrimenti crasha)
* [x] se riavvio il server dopo che il nodo è già configurato crasha (dipende dalla dimensione dei buffer - nota alla fine)
* [ ] se riavvio il server a volte non ricevo da un secondo nodo mqtt (troppo lontano?)
	* nota che se gli invio un is_alive (o un get_config) questo risponde ma è il border router che non inoltra,
		ecco perchè il server non riceve

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
* [x] eliminare funzioni di simulazione (tranne la simulazione)
* [x] il nodo 2 COAP si spaccia per più id al riavvio del server

### SERVER
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
* [x] togliere selezione protocollo e address dai comandi (prendo da cache)
* [x] fare controlli tra le cache coap e mqtt al momento della registrazione di un nodo
* [x] togliere simulazioni
* [x] ricevere dall'mqtt la configurazioen spezzata
* [x] quando invio is_alive ad un nodo mqtt che era un nodo coap, l'is_alive_ack viene considerato 
	ricevuto sia dal nodo mqtt sia coap
* [ ] fare in modo che is_alive broadcast vada a prendersi i nodi dalla cache non da mysql
* [ ] fare in modo da poter inviare is_alive broadcast anche da terminale
* [ ] killare i thread dopo che si è premuto exit
* [ ] capire perchè l'mqtt config stampa su terminale e coap no
* [ ] dopo la configurazione di un nodo coap, a volte non si salva in cache, se mand un discovery li prende
* [ ] gestire caso in cui avvengono doppie misurazioni (a volte succede)


### TEST
* [ ] fare test con 4 nodi coap
* [ ] rifare test mqtt (cooja)
* [ ] fare test con 4 nodi mqtt

### TEST FINALE
* [ ] simulazione con 2 nodi COAP e 2 nodi MQTT

### PROBLEMA SECONDARIO
* [ ] controllare che non ci siano duplicati nelle misurazioni 
* [x] se ho dei duplicati e riavvio il server python, al riavvio i nodi duplicati potrebbero prendere il posto degli
originali (rimangono attivi i listener)

### OTTIMIZZAZIONI
* [ ] cambiare il nome dei protocolli da stringhe a int


