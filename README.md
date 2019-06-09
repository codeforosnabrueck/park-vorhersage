# park-vorhersage

Dies ist ein Repository, um die Parkhaus-/Parkplatzdaten der Osnabücker
Parkstätten Betriebsgesellschaft (OPG) zu analysieren.


## Usage

Wenn ihr das Paket benutzen möchtet, müsst ihr Folgendes tun:

```python
import park_vorhersage as pv

pv.init()
pv.scrape_and_store()
```

Der oben stehende Code importiert das Paket, die `init()` Funktion erstellt
eine Datenbank und die `scrape_and_store()` Funktion stellt die eigentliche
Hauptaktion des Paketes zur Verfügung.

Da der zentrale Bestandteil des Paketes nur das Abgreifen und speichern der
Daten der OPG Website ist, ist diese Funktion besonders einfach zu erreichen.
Solltet ihr das Paket über PIP installiert haben, wird ein sogenannter
"Entry Point" generiert. Hierdurch könnt ihr nach der Installation einfach
den Befehl `parkvorhersage` auf der Kommandozeile ausführen und es wird
automatisch die Funktion `scrape_and_store()` ausgeführt.