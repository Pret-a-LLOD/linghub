# pret-a-llod

## How to import Datahub.io datasets (CKAN to CKAN)

- Log into CKAN
- Navigate to {CKAN_URL}/harvest
- Click on 'Add a harvest source'
- In the url field write the source CKAN url (https://old.datahub.io/)
- Choose a title for the harvester
- In 'Source type' select CKAN
- Set 'Update frequency to manual'
- Select the organization the datasets will belong to.
- Click save
- Navigate to the newly created harvest source (click in the name)
- Click on 'Admin' button
- Click on 'Reharvest'

## How to import TTL files (LREMap, Metashare, Clarin)

- Log into CKAN
- Navigate to {CKAN_URL}/harvest
- Click on 'Add a harvest source'
- In the url field write the url of the TTL file (the file has to be publicly accessible so CKAN can fetch it)
- Choose a title for the harvester
- In 'Source type' select 'Generic DCAT RDF Harvester'
- Set 'Update frequency to manual'
- Select the organization the datasets will belong to.
- Click save
- Navigate to the newly created harvest source (click in the name)
- Click on 'Admin' button
- Click on 'Reharvest'