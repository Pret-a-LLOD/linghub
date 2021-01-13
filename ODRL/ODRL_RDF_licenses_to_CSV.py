## RDF licenses conversion to CSV ##

# Creates a CSV from licenses defined in ODRL in the format:
# license_acronym	label	URL
# (need to install RDFlib)

import rdflib, os, csv
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, DCTERMS

# Declare the ODRL namespace
odrl = Namespace("http://www.w3.org/ns/odrl/2/")
rdflicense = Namespace("http://purl.org/NET/rdflicense/")

# Parse each ttl file to extract the information

def ttl_license_information_extraction(filepath):
	# create a Graph
	g = rdflib.Graph()

	# parse in an RDF file
	g.parse(filepath, format="ttl")

	# Looks for the policy uri, the label (dct:title if available, otherwise rdfs:label), and the verison if available
	qres = g.query(
	("PREFIX odrl: <http://www.w3.org/ns/odrl/2/>\n"
	"PREFIX rdflicense: <http://purl.org/NET/rdflicense/>\n"
	"PREFIX dct: <http://purl.org/dc/terms/>\n"
	"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
	"SELECT ?license ?title ?version WHERE {\n"
	"	   ?license a odrl:Policy . \n"
	"	   {?license rdfs:label ?title} UNION {?license dct:title ?title} . \n"
	"		OPTIONAL {?license dct:hasVersion ?version }.\n"
	"	  }"
	))
	title = ""
	license = ""

	for row in qres:
		license = str(row['license'].toPython())
		title = str(row['title'].toPython())
		if (row['version']):
			version = str(row['version'].toPython())
			title = title+", v"+version
		
	return title, license


if __name__ == "__main__":

	#ttl_license_information_extraction("/home/cecile/Documents/Pret-a-LLOD/T5.3/git_linghub_code/ODRL/ttl_licenses/afl3.0.ttl")
	# Read each ttl file to convert
	# Extract information from each file
	# Fill the future CSV

	with open('/home/cecile/Documents/Pret-a-LLOD/T5.3/git_linghub_code/ODRL/odrl_licences.csv', 'w', newline='') as csvfile:
		licenceCSV = csv.writer(csvfile, delimiter='\t')
		for file in os.listdir("/home/cecile/Documents/Pret-a-LLOD/T5.3/git_linghub_code/ODRL/ttl_licenses/"):
			if file.endswith(".ttl"):
				filepath = os.path.join("/home/cecile/Documents/Pret-a-LLOD/T5.3/git_linghub_code/ODRL/ttl_licenses/", file)
				#print(ttl_license_information_extraction(filepath))
				licenceCSV.writerow(ttl_license_information_extraction(filepath))
