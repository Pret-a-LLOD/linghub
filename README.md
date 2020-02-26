# pret-a-llod
## CKAN installation
- [CKAN](https://ckan.org/): can be [installed](https://ckan.org/download-and-install/) in 3 different ways:
- [from system packages](https://docs.ckan.org/en/latest/maintaining/installing/install-from-package.html)
- [from source code](https://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html)
- [with docker-compose](https://docs.ckan.org/en/latest/maintaining/installing/install-from-docker-compose.html)

Recommended way for further development is from source.
- Install the required packages

`sudo apt-get install python3-dev postgresql libpq-dev python3-pip python3-venv git-core solr-jetty openjdk-8-jdk redis-server`
- Install CKAN into a Python virtual environment
```
sudo mkdir -p /usr/lib/ckan/default
sudo chown whoami /usr/lib/ckan/default
python3 -m venv /usr/lib/ckan/default
. /usr/lib/ckan/default/bin/activate
```

```
pip install setuptools==36.1
pip install --upgrade pip
```
```
pip install -e 'git+https://github.com/ckan/ckan.git#egg=ckan'
pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt
```
```
deactivate
. /usr/lib/ckan/default/bin/activate
```
- Setup a PostgreSQL database

```
sudo -u postgres psql -l
sudo -u postgres createuser -S -D -R -P ckan_default
sudo -u postgres createdb -O ckan_default ckan_default -E utf-8
```
- Create a CKAN config file
```
sudo mkdir -p /etc/ckan/default
sudo chown -R `whoami` /etc/ckan/
```
`paster make-config ckan /etc/ckan/default/development.ini`

  Edit `development.ini` file:
  
    Replace pass with the password that you created in 3:
    `sqlalchemy.url = postgresql://ckan_default:pass@localhost/ckan_default`
    
    *Tip: If you’re using a remote host with password authentication rather than SSL authentication, use: `sqlalchemy.url = postgresql://ckan_default:pass@<remotehost>/ckan_default?sslmode=disable`*

    `ckan.site_id = default`: Each CKAN site should have a unique `site_id`
    
    Replace by the site’s URL (used when putting links to the site into the FileStore, notification emails etc. Do not add a trailing slash to the URL:
     `ckan.site_url = http://demo.ckan.org`

- Setup Solr
  
  _If using Ubuntu 18.04 do:  
    `sudo ln -s /etc/solr/solr-jetty.xml /var/lib/jetty9/webapps/solr.xml`
    Then edit the `jetty.port` value in `/etc/jetty9/start.ini`:
      `jetty.port=8983  # (line 23)`_
      
  **WARNING** If installing a version of CKAN higher than 1.7 with *Ubuntu 18.04*, you have to use Solr directly, without jetty as there is an issue (https://github.com/ckan/ckan/issues/4762):
  
  -  First clean any jetty-related things (if you have them), as per the explanations here:  https://github.com/ckan/ckan/issues/4762#issuecomment-496907286
  - Second, instead of 1. below, install Solr as per the instructions given here: https://github.com/ckan/ckan/wiki/Install-and-use-Solr-6.5-with-CKAN
  - In 3. below, replace the `sudo service jetty9 restart` command by `sudo service solr restart`

 1. Edit Jetty configuration file (`/etc/default/jetty8(9)` or `/etc/default/jetty`) and change the following variables:

    ```
    NO_START=0            # (line 4)
    JETTY_HOST=127.0.0.1  # (line 16)
    JETTY_PORT=8983       # (line 19)
    ```
    Start or restart the Jetty server.
      For Ubuntu 18.04: `sudo service jetty9 restart`, for Ubuntu 16.04: `sudo service jetty8 restart`

    You can test Solr responds correctly with `curl http://localhost:8983/solr/`

2. Replace the default `schema.xml` file with a symlink to the CKAN schema file included in the sources.

    ```
    sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
    sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
    ```
    Restart solr:
    For Ubuntu 18.04: `sudo service jetty9 restart`
    For Ubuntu 16.04: `sudo service jetty8 restart`
    
    Check that Solr is running by opening http://localhost:8983/solr/.

3. Change the `solr_url` setting in CKAN configuration file (`/etc/ckan/default/production.ini`) to point to your Solr server, for example:

  ` solr_url=http://127.0.0.1:8983/solr`


- Link to who.ini

`ln -s /usr/lib/ckan/default/src/ckan/who.ini /etc/ckan/default/who.ini`
- Create database tables
```
cd /usr/lib/ckan/default/src/ckan
paster db init -c /etc/ckan/default/development.ini
```
- Set up [DataStore](https://docs.ckan.org/en/latest/maintaining/datastore.html#setting-up-the-datastore) (not needed in LingHub)

For a further explanation of the above installation process refer to [Install CKAN from source](https://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html)

After completing the installation process there are few extensions to be installed.


### Extensions 
CKAN mandatory extensions for the pret-a-llod project are:
- stats *
- text_view *
- image_view *
- recline_view *
- [harvest](https://github.com/ckan/ckanext-harvest). Provides:
  - ckan_harvester
  - csw_harvester
  - waf_harvester
  - doc_harvester
  - dcat_rdf_harvester
  - dcat_json_harvester
- [dcat](https://github.com/ckan/ckanext-dcat)
  - dcat_json_interface
- [scheming_datasets](https://github.com/ckan/ckanext-scheming)

\* Included in core CKAN

Install them using their relevant instructions. They will be installed in the folder `src` at the python_env location (`/usr/lib/ckan/default/`)

Navigate to `{CKAN_URL}/api/action/status_show` for a list of enabled extensions.


Once these extensions are installed and configured we can start the datasets harvesting process.

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
