# script to convert the format of CLARIN metadata dump to Dublin Core/DCAT
import lxml.etree as ET
import os, sys
from fnmatch import fnmatch

def convert_XML_file (xml_in_filename):
	xsl_filename = "/home/cecile/Documents/Pret-a-LLOD/T5.3/new_linghub_code/scripts/metadata_conversion/clarin2dcat.xsl"

	dom = ET.parse(xml_in_filename)
	xslt = ET.parse(xsl_filename)
	transform = ET.XSLT(xslt)
	newdom = transform(dom)
	print (ET.tostring(newdom, pretty_print=True))

	return ET.tostring(newdom, pretty_print=True)

# Recurse and process files.
def process(src_dir, dst_dir, pattern='*.xml'):
	"""Iterate through src_dir, processing all files that match pattern and
	store them, including their parent directories in dst_dir.
	"""
	assert src_dir != dst_dir, 'Source and destination dir must differ.'
	for dirpath, dirnames, filenames in os.walk(src_dir):
		# Filter out files that match pattern only.
		filenames = filter(lambda fname: fnmatch(fname, pattern), filenames)

		if filenames:

			# remove the static source path from dirpath, to keep only the rest of the folder hierarchy
			dirpath=dirpath.replace(src_dir,'')

			# create the destination directior
			dir_ = os.path.join(dst_dir, dirpath)
			if not os.path.exists(dir_):
				os.makedirs(dir_)
			for fname in filenames:
				in_fname = os.path.join(dirpath, fname)
				out_fname = os.path.join(dir_, fname)
				# convert and print each DCAT-converted file
				#convert_XML_file(in_fname, out_fname)


if __name__ == "__main__":

	xml_folder = "/home/cecile/Documents/Pret-a-LLOD/T5.3/data/clarin/results/cmdi/"

	output_folder="/home/cecile/Documents/Pret-a-LLOD/T5.3/data/clarin/results/dcat_format/"

	#process(xml_folder, output_folder)
	print (convert_XML_file("/home/cecile/Documents/Pret-a-LLOD/T5.3/data/clarin/results/cmdi/ARCHE/http_hdl_handle_net_21_11115_0000_000C_35DA_3.xml"))

