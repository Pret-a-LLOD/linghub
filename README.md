# pret-a-llod
## CKAN installation (use version 2.8.4.)
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

For version 2.8.4 (working version for LingHub):`pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.8.4#egg=ckan'`

(for the latest version:`pip install -e 'git+https://github.com/ckan/ckan.git#egg=ckan'`)

`pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt`

```
deactivate
. /usr/lib/ckan/default/bin/activate
```

- Install RabbitMQ using Systemctl 
```
https://tecadmin.net/install-rabbitmq-server-on-ubuntu/
(stop at the "sudo systemctl start rabbitmq-server" command)
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
    
    Add the following:
     
      `##Carrot Messagin Library
      carrot_messaging_library=pika
      amqp_hostname=localhost
      amqp_port=5672
      amqp_user_id=guest
      amqp_password=guest`


- Setup Solr
  
 ##check if needed _If using Ubuntu 18.04 do:  
 ##`sudo ln -s /etc/solr/solr-jetty.xml /var/lib/jetty9/webapps/solr.xml`

 1. Edit Jetty configuration file 
 
      - Ubuntu 16 or under Either in: `/etc/default/jetty8(9)` or `/etc/default/jetty`) and change the following variables:

        ```
        NO_START=0            # (line 4)
        JETTY_HOST=127.0.0.1  # (line 16)
        JETTY_PORT=8983       # (line 19)
        ```
      - Ubuntu 18.04 of above: in `/etc/jetty9/start.ini`  and change the following variables:  
        ```
        jetty_host=127.0.0.1 #localhost
        jetty_port=8983  # previously 8080
        ```
								
    	Start or restart the Jetty server.
					
								- For Ubuntu 18.04: ```sudo service jetty9 restart`, for Ubuntu 16.04: ````sudo service jetty8 restart```

    You can test Solr responds correctly with `curl http://localhost:8983/solr/` (will probably give an error, see next step)
    
 1. (ubuntu 18.04) Solve the issue linked to installing a CKAN version above 1.7 and using Ubuntu 18.04 or later, as per solution given in  (https://github.com/ckan/ckan/issues/4762):
 
       - ``` sudo mkdir /etc/systemd/system/jetty9.service.d ```
        
       - Create a new configuration file for solr
       
        sudo nano /etc/systemd/system/jetty9.service.d/solr.conf
        
       - and add 
        
        [Service]
        ReadWritePaths=/var/lib/solr
        
       - Then
       ```sudo nano /etc/solr/solr-jetty.xml``` and replace with the below configuration.
       
       solr-jetty.xml
       ```
       <?xml version="1.0"  encoding="ISO-8859-1"?>
       <!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN" "http://www.eclipse.org/jetty/configure.dtd">

       <!-- Context configuration file for the Solr web application in Jetty -->

       <Configure class="org.eclipse.jetty.webapp.WebAppContext">
         <Set name="contextPath">/solr</Set>
         <Set name="war">/usr/share/solr/web</Set>

         <!-- Set the solr.solr.home system property -->
         <Call name="setProperty" class="java.lang.System">
           <Arg type="String">solr.solr.home</Arg>
           <Arg type="String">/usr/share/solr</Arg>
         </Call>

         <!-- Enable symlinks -->
         <!-- Disabled due to being deprecated
         <Call name="addAliasCheck">
           <Arg>
             <New class="org.eclipse.jetty.server.handler.ContextHandler$ApproveSameSuffixAliases"/>
           </Arg>
         </Call>
         -->
       </Configure>
       ```
							
       - You may have to reload the system with ```systemctl daemon-reload```
							
       - Restart jetty9 ```sudo service jetty9 restart ```
							
       Check if it is working by opening a browser and type the url: ```http://140.203.155.44:8983/solr``` 
        

2. Replace the default `schema.xml` file with a symlink to the CKAN schema file included in the sources.

    ```
    sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
    sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
    ```
    Restart solr:
    For Ubuntu 18.04: `sudo service jetty9 restart`
    For Ubuntu 16.04: `sudo service jetty8 restart`
    
    Check that Solr is running by opening http://140.203.155.44:8983/solr/.

3. Change the `solr_url` setting in CKAN configuration file (`/etc/ckan/default/development.ini`) to point to your Solr server, for example:

  ` solr_url=http://127.0.0.1:8983/solr` (localhost)


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
- [ckanext-harvest](https://github.com/ckan/ckanext-harvest). Provides:
  - ckan_harvester
  - dcat_rdf_harvester
  - dcat_json_harvester
- [ckanext-dcat](https://github.com/ckan/ckanext-dcat). Provides:
  - dcat
  - dcat_rdf_harvester
  - dcat_json_harvester
  - dcat_json_interface

\* Included in core CKAN

Install them using their relevant instructions. They will be installed in the folder `src` at the python_env location (`/usr/lib/ckan/default/`)

Navigate to `{CKAN_URL}/api/action/status_show` for a list of enabled extensions.


Once these extensions are installed and configured we can start the datasets harvesting process.


## How to import datasets from a CKAN-based platform to our own CKAN platform (example with Datahub.io datasets)
1. Log into CKAN UI with your ckan user details 

(note that you have to be a sysadmin. 
To do so, execute the follwing command `paster --plugin=ckan sysadmin add cecrob --config=/path/to/development.ini` - generally `/path/to/` is `/etc/ckan/default/`)

2. Navigate to `{CKAN_URL}/harvest`
3. Click on 'Add a harvest source'
4. In the url field write the source CKAN url ` https://datahub.ckan.io`
5. Choose a title for the harvester
6. In 'Source type' select CKAN
7. Set 'Update frequency to manual'
8. Select the organization the datasets will belong to (you need to have the organization created beforehand in `{CKAN_URL}/organization/`)
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
