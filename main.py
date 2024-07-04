import os
import json
import xml.etree.ElementTree as ET
from google.cloud import storage
from flask import escape

def xml_to_dict(element):
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

def convert_xml_to_json(event, context):
    # Replace with your bucket name
    bucket_name = 'your-bucket-name'

    # Get file names from the event
    xml_file_name = event['name']
    json_file_name = xml_file_name.replace('.xml', '.json')

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Download XML file from GCS
    blob = bucket.blob(xml_file_name)
    xml_content = blob.download_as_string()
    
    # Parse XML and convert to dictionary
    root = ET.fromstring(xml_content)
    data_dict = {root.tag: xml_to_dict(root)}
    
    # Convert dictionary to JSON string
    json_content = json.dumps(data_dict, ensure_ascii=False, indent=4)
    
    # Upload JSON file to GCS
    json_blob = bucket.blob(json_file_name)
    json_blob.upload_from_string(json_content, content_type='application/json')
    
    return f"Converted {xml_file_name} to {json_file_name} and uploaded to {bucket_name}"

