'''Title: dct:title
Language: dct:language
Rights: ODRL or dct:rights or dct:accessRights or dct:license
Type: dct:type
Creator: dct:creator
Source: dct:source
Contributor: dct:contributor
Subject: dct:subject
Description: dct:description
accessUrl: foaf:homePage (for dcat:Catalog) or dcat:landingPage (for dcat:Dataset) or dcat:downloadUrl (for a dcat:Distribution) or dcat:endPointUrl (dcat:DataService)
contactPoint: dcat:contactPoint'''

"""
Given a turtle file yields which lines will not be parsed according to
https://github.com/ckan/ckanext-dcat#rdf-dcat-to-ckan-dataset-mapping
hence won't be imported into the CKAN dataset
"""

# Standard library imports
import re
import argparse
# Third party imports

# Local application imports


def get_datasets(f):
    with open(f, 'r') as the_file:
        contents = the_file.read()
    datasets = contents.split('\n\n')

    return datasets


def check_dcat(dataset):
    fixed_line = ''
    parsed = []
    not_parsed = []
    dcat_subjects = ['dct:title', 'dct:description', 'dcat:keyword', 'dcat:theme', 'dct:identifier',
                     'adms:identifier', 'dct:issued', 'dct:modified', 'owl:versionInfo', 'adms:versionNotes',
                     'dct:language', 'dcat:landingPage', 'dct:accrualPeriodicity', 'dct:conformsTo',
                     'dct:accessRights', 'foaf:page', 'dct:provenance', 'dct:type', 'dct:hasVersion',
                     'dct:isVersionOf', 'dct:source', 'adms:sample', 'dct:spatial', 'dct:temporal', 'dct:publisher',
                     'foaf:name', 'foaf:mbox', 'foaf:homepage', 'dct:type', 'dcat:contactPoint', 'vcard:fn',
                     'vcard:hasEmail', 'dcat:distribution', 'dct:title', 'dcat:accessURL', 'dcat:downloadURL',
                     'dct:description', 'dcat:mediaType', 'dct:format', 'dct:license', 'adms:status', 'dcat:byteSize',
                     'dct:issued', 'dct:modified', 'dct:rights', 'foaf:page', 'dct:language', 'dct:conformsTo',
                     'spdx:checksumValue', 'spdx:algorithm', 'a']
    for line in dataset.splitlines():
        if fixed_line:
            line = fixed_line + line
            fixed_line = ''
        if len(line.strip()) == 0 or line.lstrip().startswith('<http://linghub'):
            pass
        else:
            try:
                ttl_subject, ttl_predicate, ttl_object = re.findall("(?:\".*?\"|\S)+", line)
                if ttl_subject in dcat_subjects:
                    parsed.append(line)
                else:
                    not_parsed.append(line)
            except:
                # removing trailing line break
                fixed_line = line.replace('\n', '', 1)

    return parsed, not_parsed


def write_to_file(text):
    with open('output.txt', 'w') as the_file:
        the_file.write(text)


def main(ttl_file):
    output = ''
    datasets = get_datasets(ttl_file)
    for dataset in datasets[1:]:
        parsed, not_parsed = check_dcat(dataset)
        output += dataset
        output += f'\nTotal triples\tParsed\tNot parsed\n{len(parsed) + len(not_parsed)}\t\t\t\t{len(parsed)}\t\t{len(not_parsed)}\n'
        for np in not_parsed:
            output += np + '\n'
        output += '\n'
    write_to_file(output)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="file to process")
    args = vars(ap.parse_args())
    main(args['file'])

