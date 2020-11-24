#coding=utf8
import sys
import re
import os

##################################################################
##  RDF_to_SAF_converter.py     
## ---------------------------------------------                                 
## Convert an XML/RDF file to the format read by DSpace:
## Simple Archive Format
## Note: This converts only metadata formats that
## are following the community standards established in
## the Pret-a-LLOD project (https://pret-a-llod.github.io/)
## ie. the metadata in the RDF/XML need to be converted 
## to these standards first
## ------------------------------------------------
## Usage:
##    argument 1: rdf file
##    argument 2: output folder path

##################################################################


# Create a name for each xml file corresponding to each metadata namespace for each item
# List of possible formats:
# dc  http://dublincore.org/documents/dcmi-terms/  -> Note that http://purl.org/dc/terms/ and http://purl.org/dc/elements/1.1/ both belong to dcmi-terms!
# ODRL  http://www.w3.org/ns/odrl/2/
# dcat  http://www.w3.org/ns/dcat#
# owl http://www.w3.org/2002/07/owl#
# rdf http://www.w3.org/1999/02/22-rdf-syntax-ns#
# rdfs  http://www.w3.org/2000/01/rdf-schema#
# skos  http://www.w3.org/2004/02/skos/core#
# foaf  http://xmlns.com/foaf/0.1/
# olac  http://www.language-archives.org/OLAC/1.1/
# oaidc   http://www.openarchives.org/OAI/2.0/oai_dc/
# ms  http://purl.org/net/def/metashare


dc_xml = 'dublin_core.xml'
ODRL_xml = 'metadata_ODRL.xml'
dcat_xml = 'metadata_dcat.xml'
owl_xml = 'metadata_owl.xml'
rdf_xml = 'metadata_rdf.xml'
rdfs_xml = 'metadata_rdfs.xml'
skos_xml = 'metadata_skos.xml'
foaf_xml = 'metadata_foaf.xml'
olac_xml = "metadata_olac.xml"
oaidc_xml = "metadata_oaidc.xml"
ms_xml = "metadata_ms.xml"


#create a dictionary for each metadata formats string
# note that both dc and dct belong to dcmi-terms
metadata_format = {
    "http://purl.org/dc/elements/1.1/": "dc",
    "http://purl.org/dc/terms/": "dct"
    "http://www.w3.org/ns/odrl/2/": "ODRL"
    "http://www.w3.org/ns/dcat#": "dcat"
    "http://www.w3.org/2002/07/owl#": "owl"
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf"
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs"
    "http://www.w3.org/2004/02/skos/core#": "skos"
    "http://xmlns.com/foaf/0.1/": "foaf"
    "http://www.language-archives.org/OLAC/1.1/": "olac"
    "http://www.openarchives.org/OAI/2.0/oai_dc/": "oaidc"
    "http://purl.org/net/def/metashare": "ms"
}

if len(sys.argv) > 2:
    print("Too many arguments. Please provide: \nfilename: The rdf file to convert (as rdf, rdfs, owl, n3, ttl, nt, trix, xhtml, html, svg, nq or trig).\noutput: The output directry")
    exit()

if not isinstance(sys.argv[1], str):
    print("Error on arguments. Please provide: \nfilename: The rdf file to convert (as rdf, rdfs, owl, n3, ttl, nt, trix, xhtml, html, svg, nq or trig).\noutput: The output directry")
    exit()

if not sys.argv[1].endswith(".rdf"):
    print("Error on arguments. Please provide: \nfilename: The rdf file to convert (as rdf, rdfs, owl, n3, ttl, nt, trix, xhtml, html, svg, nq or trig).\noutput: The output directry")
    exit()

rdf_input_file = sys.argv[1]
out_dir = sys.argv[2]

# Open the rdf file (Any of: rdf, rdfs, owl, n3, ttl, nt, trix, xhtml, html, svg, nq, trig)

print (guess_format(rdf_input_file))

# Count the number of resources
# Extracts the metadata schema
# Read each resource (item)
    # For each resource
        # Make a numbered directory for the item (starting from item_000/ <- put as many 0s as the maximum number of resource needs)
        # For each metadata schema
            # Create a xml file per metadata  schema on the following model:
            # <?xml version="1.0" encoding="UTF-8"?>
            # <dublin_core schema="dcat">  <--- add "schema= XXX" for all schema that is not dublin_core
            #      <dcvalue element="degree" qualifier="department">Computer Science</dcvalue>
            #      <dcvalue element="degree" qualifier="level">Masters</dcvalue>
            # </dublin_core>

                # For each metadata schema
                    # Extract the "element", "qualifier" (if present), and value
                    # Fill the xml with this info
                    # Print the xml



## Based on :
# with open(filename, "r") as f:
#   content = f.read()
#  Convert RDF Dublin Core to DSpace Dublin Core Simple Archive Format
#   content = re.sub(r'\s\s<(\/?)rdf:Description', r'<\1dublin_core', content)
#   content = re.sub(r'(\.|\s|\,|\/)*</dc:.+>', r'</dcvalue>', content)
#   content = re.sub(r'\s\s<dc:(\w+)>', r'<dcvalue element="\1">', content)
#   content = re.sub(r'<(\/)?rdf:RDF.*>', '', content)

#   # Convert some elements to supported DSpace elements
#   content = re.sub(r'element="creator"', r'element="contributor" qualifier="author"', content)
#   content = re.sub(r'element="date"', r'element="date" qualifier="issued"', content)
#   content = re.sub(r'element="identifier"', r'element="relation" qualifier="uri"', content)
#   content = re.sub(r'element="format"', r'element="format" qualifier="mimetype"', content)
#   content = re.sub(r'element="type">.*?</dcvalue>', r'element="type">เอกสารสิ่งพิมพ์</dcvalue>', content)
#   content = re.sub(r'element="language">tha</dcvalue>', r'element="language">th</dcvalue>', content)

#   # Create Simple Archive Structure to be imported to DSpace
#   os.mkdir(BOOK_ARCHIVE_DIR_NAME)
#   os.mkdir(VDO_ARCHIVE_DIR_NAME)

#   # Extract each item to create its own directory structure
#   book_count = 0
#   vdo_count = 0
#   for idx, item in enumerate(re.findall(r'(<dublin_core>.*?</dublin_core>)', content, flags=re.DOTALL)):
#       if 'healthstation.in.th' in item:
#           archive_dir = VDO_ARCHIVE_DIR_NAME
#           vdo_count += 1
#           count = vdo_count
#           item = re.sub(r'element="type">.*?</dcvalue>', r'element="type">สื่อมัลติมีเดีย</dcvalue>', item)
#           item = re.sub(r'</dublin_core>', r'  <dcvalue element="subject" qualifier="classification">VDO</dcvalue>\n</dublin_core>', item)
#           item = re.sub(r'(<dcvalue element="relation" qualifier="uri">.+)</dcvalue>', r'\1/</dcvalue>', item)
#       else:
#           archive_dir = BOOK_ARCHIVE_DIR_NAME
#           book_count += 1
#           count = book_count
#       item_dir = archive_dir + '/item_' + str(count).zfill(5)
#       os.mkdir(item_dir)
#       with open(item_dir + '/'+ DUBLIN_CORE_FILE_NAME, 'w') as xml_file:
#           xml_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
#           xml_file.write(item + '\n')

#       # Create empty contents file that is mandatory for importing to DSpace
#       # (Actually, this file is used to specify bistream file names)
#       open(item_dir + '/' + CONTENTS_FILE_NAME, 'w').close()

