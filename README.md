# pret-a-llod
## CKAN installation
- CKAN: https://ckan.org/ can be installed https://ckan.org/download-and-install/ in 3 different ways:
- from system packages https://docs.ckan.org/en/latest/maintaining/installing/install-from-package.html
- from source code https://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html
- with docker-compose https://docs.ckan.org/en/latest/maintaining/installing/install-from-docker-compose.html

Recommended way for further development is from source. After completing the installation process there are few extensions to be installed.

### Extensions 
CKAN mandatory extensions for the pret-a-llod project are:
- sqlalchemythread
- uwsgistats
- stats
- text_view
- image_view
- recline_view
- dcat
- dcat_json_interface
- scheming_datasets
- spatial_metadata
- spatial_query
- harvest
- ckan_harvester
- csw_harvester
- waf_harvester
- doc_harvester
- dcat_rdf_harvester
- dcat_json_harvester

Harvest extension: https://github.com/ckan/ckanext-harvest

DCAT extension https://github.com/ckan/ckanext-dcat

Once this 2 extensions are installed and configured we can start the datasets harvesting process.

## How to import Datahub.io datasets (CKAN to CKAN)
- Log into CKAN
- Navigate to `{CKAN_URL}/harvest`
- Click on 'Add a harvest source'
- In the url field write the source CKAN url `https://old.datahub.io/`
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
- Navigate to `{CKAN_URL}/harvest`
- Click on 'Add a harvest source'
- In the url field write the url of the TTL file (the file has to be publicly accessible so CKAN can fetch it)
- Choose a title for the harvester
- In 'Source type' select 'Generic DCAT RDF Harvester'
- Set 'Update frequency to manual'
- In 'Configuration' write `{"rdf_format":"turtle"}`
- Select the organization the datasets will belong to.
- Click save
- Navigate to the newly created harvest source (click in the name)
- Click on 'Admin' button
- Click on 'Reharvest'