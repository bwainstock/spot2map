spot2map
========

Plots Spot personal locator beacon data onto map using Leaflet.js

Requires a PostGIS enabled database
	docker run --expose=5432 --name postgis -e POSTGRES_PASSWORD=password -e POSTGRES_DB=pct_spot -d mdillon/postgis	
	docker inspect postgis | grep \"IPAddress\"
