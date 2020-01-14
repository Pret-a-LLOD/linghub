# pret-a-llod
## CKAN installation
- [CKAN](https://ckan.org/): can be [installed](https://ckan.org/download-and-install/) in 3 different ways:
- [from system packages](https://docs.ckan.org/en/latest/maintaining/installing/install-from-package.html)
- [from source code](https://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html)
- [with docker-compose](https://docs.ckan.org/en/latest/maintaining/installing/install-from-docker-compose.html)

Recommended way for further development is from source.

After completing the installation process there are few extensions to be installed.

### Extensions 
CKAN mandatory extensions for the pret-a-llod project are:
- datastore *
- datapusher *
- datatablesview *
- sqlalchemythread *
- uwsgistats *
- stats *
- text_view *
- image_view *
- recline_view *
- harvest
- ckan_harvester
- csw_harvester
- waf_harvester
- doc_harvester
- dcat_rdf_harvester
- dcat_json_harvester
- dcat
- dcat_json_interface
- scheming_datasets

\* Included in core CKAN

Navigate to `{CKAN_URL}/api/action/status_show` for a list of enabled extensions.

[Harvest extension](https://github.com/ckan/ckanext-harvest)

[DCAT extension](https://github.com/ckan/ckanext-dcat)

[Scheming extension](https://github.com/ckan/ckanext-scheming)

Once this extensions are installed and configured we can start the datasets harvesting process.

## How to import Datahub.io datasets (CKAN to CKAN)
1. Log into CKAN
2. Navigate to `{CKAN_URL}/harvest`
3. Click on 'Add a harvest source'
4. In the url field write the source CKAN url `https://old.datahub.io/`
5. Choose a title for the harvester
6. In 'Source type' select CKAN
7. Set 'Update frequency to manual'
8. Select the organization the datasets will belong to
9. Click save
10. Navigate to the newly created harvest source (click in the name)
11. Click on 'Admin' button
12. Click on 'Reharvest'

## How to import TTL files (LREMap, Metashare, Clarin)
1. Log into CKAN
2. Navigate to `{CKAN_URL}/harvest`
3. Click on 'Add a harvest source'
4. In the url field write the url of the TTL file (the file has to be publicly accessible so CKAN can fetch it)
5. Choose a title for the harvester
6. In 'Source type' select 'Generic DCAT RDF Harvester'
7. Set 'Update frequency to manual'
8. In 'Configuration' write `{"rdf_format":"turtle"}`
9. Select the organization the datasets will belong to
10. Click save
11. Navigate to the newly created harvest source (click in the name)
12. Click on 'Admin' button
13. Click on 'Reharvest'