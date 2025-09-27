import os
from typing import Optional
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
load_dotenv()

def upload_to_blob(file_bytes: bytes, blob_name: str) -> Optional[str]:
    """
    Upload file bytes to Azure Blob if env vars are present.
    Returns the blob URL or None if disabled.
    """
    conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container = os.getenv("AZURE_BLOB_CONTAINER")
    if not (conn and container):
        return None
    try:
        svc = BlobServiceClient.from_connection_string(conn)
        container_client = svc.get_container_client(container)
        # Ensure container exists (won't fail if already present)
        try:
            container_client.create_container()
        except Exception:
            pass
        blob = container_client.get_blob_client(blob_name)
        blob.upload_blob(file_bytes, overwrite=True)
        # Form URL if account name is in the connection string
        # Fallback to blob.url property
        return blob.url
    except Exception as e:
        return f"Blob upload failed: {e}"
