import xml.etree.ElementTree as ET
import json

def xml_to_dict(element):
    """
    Convert an XML element and its children into a dictionary.
    """
    node = {}
    if element.text:
        node['text'] = element.text.strip()
    for child in element:
        child_dict = xml_to_dict(child)
        if child.tag in node:
            if not isinstance(node[child.tag], list):
                node[child.tag] = [node[child.tag]]
            node[child.tag].append(child_dict)
        else:
            node[child.tag] = child_dict
    return node

def convert_xml_to_json(xml_file, json_file):
    """
    Convert the given XML file to a JSON file.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data_dict = {root.tag: xml_to_dict(root)}
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

# Define file names
xml_file = 'example.xml'
json_file = 'output.json'

# Convert XML to JSON
convert_xml_to_json(xml_file, json_file)

print(f"Converted {xml_file} to {json_file}")
