# ToosoCodingAssignment

Prendendo ispirazione da questo articolo https://medium.com/@wolfgarbe/1000x-faster-spelling-correction-algorithm-2012-8701fcd87a5f ho modificato il spellchecker di Norvig faccendo le seguenti modifiche:
- Aggiunto un dictionary DeletedWords1 chiave:{valore} dove le chiavi sono le parole del dictionary WORDS modificate con una cancellazione. E il valore e un set delle parole originali. Es. sn:{sun,sin}
- Aggiunto un dictionary DeletedWords2 applicando la stessa logica al dictionary DeletedWords1.
- Modificato le funzioni edits1 e edits2, che calcolavano tutte le possibili combinazione di stringe a distanza 1/2 da una stringa originale in input, per calcolare le possibili combinazioni di stringe a distanza uno o due usando solo la operazione di cancellazione.
- aggiunte due funzioni knowndis1 e knowndis2 che partendo da una lista di stringa restituiscono tutte le parole valide usando i due nuovi dict DeletedWords1 e DeletedWords2.
- modificato la funzione candidates per prendere in considerazione l'aggiunta dei due nuovi dict e per considerare tutti i casi perche' le cancellazioni si devono applicare anche alla parola originale e non basta usare solo i due nuovi dizionari
Usando lo stesso modello di linguagio e i stessi test che usa Norvig nel suo spellchecker i risultati sono 
Per il spellchecker di Norvig:
75% of 270 correct (6% unknown) at 33 words per second 
68% of 400 correct (11% unknown) at 29 words per second 
Per il spellchecker modificato:
77% of 270 correct (6% unknown) at 24182 words per second 
70% of 400 correct (11% unknown) at 22107 words per second 

Il miglioramento in termini di performance viene dal precalcolo che si fa nella creazione delle due dict DeletedWords1 e DeletedWords2.
Il piccolo miglioramento in termini di correttezza viene dal semplice fatto che con il nuovo modo di calcolare le distanze si possono 'indovinare' parole con distanca 3 senza troppe perdite di performance.
