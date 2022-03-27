#! /home/mluser/projects/Keywork-Extraction-Kaggle-Stackoverflow/env/bin


from ast import Raise
from load_config import KEYS
from tqdm import tqdm
from azure.storage.blob import ContainerClient, BlobServiceClient
import os, argparse, tqdm

def upload(connection_string, container_name, filename, path):
    container_client = ContainerClient.from_connection_string(connection_string, container_name)
    
    print(f"Upload to container: '{container_name}' is in progress... \n")
    
    blob_client = container_client.get_blob_client(filename)
    #print("This ->> ", os.path.join(path, filename))
    with open(os.path.join(path, filename), "rb") as data:
        blob_client.upload_blob(data)

    print("File upload complete")

def download(connection_string, container_name, filename, path):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(filename)
    
    print(f"Setting up connection with blob... \n")
    print(filename)
    stream_downloaded = blob_client.download_blob()
    print(f"Writing to file '{container_name}' is in progress... \n")
    
    with open(os.path.join(path, filename), "wb") as data:
        data.write(stream_downloaded.readall())
    
    print("File download complete")


if __name__ == "__main__":

    # get the secrets and other config from config file
    keys = KEYS()
    STORAGE = keys.AZURE["STORAGE_ACCOUNTS"]
    APP = keys.APP
    
    #print("==USING STORAGE KEYS==")
    #print(STORAGE.keys())
    #print("\n==USING APP CONFIGURATIONS==")
    #print(APP)

    # get keyword arguments
    parser = argparse.ArgumentParser(description="Script to upload or download data to specified azure blob")
    parser.add_argument("--operation", type = str)
    parser.add_argument("--filename", type = str)   # source / destination file name

    # get the arguments
    args = parser.parse_args()

    if args.operation == "upload":
        upload(STORAGE["CONNECTION_STRING"], STORAGE["CONTAINER_NAME"], args.filename, path = APP["ROOT"] + APP["INPUT"])
    elif args.operation == "download":
        download(STORAGE["CONNECTION_STRING"], STORAGE["CONTAINER_NAME"], args.filename, path = APP["ROOT"] + APP["INPUT"])
    else:
        raise ValueError("Value of operation is: [upload, download]")
