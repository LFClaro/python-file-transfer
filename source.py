import os
import time
import requests
import xml.etree.ElementTree as ET
from multiprocessing import Process
# from flask import Flask, send_from_directory

path = os.getcwd()
PUT_ROUTE = 'uploads'
DELETE_ROUTE = 'delete'
UPLOAD_FOLDER = os.path.join(path, PUT_ROUTE)
SERVER_URL = 'http://localhost:8081/'

# Make directory for uploads if it doesn't exist
if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f'{UPLOAD_FOLDER} created')

def putBinary(fileNames,url):
    files = []
    for fileName in fileNames:
        files.append(('files', open(f'{UPLOAD_FOLDER}/{fileName}', 'rb')))
        
    response = requests.put(url, files=files)

    return response

def deleteBinary(x, fileNames, url):
    time.sleep(x)

    files = []
    for fileName in fileNames:
        files.append(('files', open(f'{UPLOAD_FOLDER}/{fileName}', 'rb')))
    response = requests.delete(url, files=files)

    return response

def create_v_a(x):
    i = 0
    while True:
        if os.path.exists(f'{UPLOAD_FOLDER}/V{i}.mp4') and os.path.exists(f'{UPLOAD_FOLDER}/V{i}.mp4'):
            i += 1
        else:
            open(f'{UPLOAD_FOLDER}/V{i}.mp4', "w")
            open(f'{UPLOAD_FOLDER}/A{i}.mp4', "w")
            print(f'V{i}.mp4 and A{i}.mp4 CREATED')

            try:
                doc = ET.parse(f'{UPLOAD_FOLDER}/mpdFile.xml')
                root = doc.getroot()
                data = root
            except FileNotFoundError:
                data = ET.Element('files')
                print(f'mpdFile.xml CREATED')

            element = ET.SubElement(data, f'upload')

            sub_elem1 = ET.SubElement(element, f'V{i}')
            sub_elem2 = ET.SubElement(element, f'A{i}')
            sub_elem1.text = f'V{i}.mp4'
            sub_elem2.text = f'A{i}.mp4'
            
            tree = ET.ElementTree(data)
            tree.write(f'{UPLOAD_FOLDER}/mpdFile.xml')

            uploadedFiles = [f'V{i}.mp4', f'A{i}.mp4', 'mpdFile.xml']

            response = putBinary(uploadedFiles, SERVER_URL+PUT_ROUTE)

            if response.status_code != 400:
                print(response.text)
                # Keeping 'mpdFile.xml' and deleting the other files after 10 seconds
                for file in uploadedFiles[:-1]:
                    delete_response = Process(target=deleteBinary, args=(10, uploadedFiles, f'{SERVER_URL}{DELETE_ROUTE}/{file}',))
                    delete_response.start()
            else:
                print(response.text)
                break

            time.sleep(x)
        
def create_c(x):
    j = 0
    while True:
        if os.path.exists(f'{UPLOAD_FOLDER}/C{j}.mp4'):
            j += 1
        else:
            time.sleep(x)
            open(f'{UPLOAD_FOLDER}/C{j}.mp4', "w")
            print(f'C{j}.mp4 CREATED')

            try:
                doc = ET.parse(f'{UPLOAD_FOLDER}/mpdFile.xml')
                root = doc.getroot()
                data = root
            except FileNotFoundError:
                data = ET.Element('files_list')

            element = ET.SubElement(data, f'file')

            sub_elem1 = ET.SubElement(element, f'C{j}')
            sub_elem1.text = f'C{j}.mp4'

            tree = ET.ElementTree(data)
            tree.write(f'{UPLOAD_FOLDER}/mpdFile.xml')

            uploadedFiles = [f'C{j}.mp4', 'mpdFile.xml']
            
            response = putBinary(uploadedFiles, SERVER_URL+PUT_ROUTE)

            if response.status_code != 400:
                print(response.text)
                # Keeping 'mpdFile.xml' and deleting the other files after 10 seconds
                for file in uploadedFiles[:-1]:
                    delete_response = Process(target=deleteBinary, args=(10, uploadedFiles, f'{SERVER_URL}{DELETE_ROUTE}/{file}',))
                    delete_response.start()
            else:
                print(response.text)
                break

# Multiprocessing supports spawning processes using an API similar to the threading module.
process1 = Process(target=create_v_a, args=(2,))
process2 = Process(target=create_c, args=(360,))

# Inserting guard in the main module to avoid creating subprocesses recursively
if __name__ == '__main__':   
    process1.start()
    process2.start()