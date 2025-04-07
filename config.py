# config.py
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=mydatastoragexyz;AccountKey=tRRero1Uvt9Kw9LYDucDftquu8VcMFKepXHUVWw8uAlslZgiobYQlsG34vH4uBnCBKuQC61ENeUd+AStJBCuLw==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "dataset"

# Define dataset file paths in Azure Storage
timeframe_files = [
    "Gold_1min_25_15.csv",
    "Gold_5min_25_10.csv",
    "Gold_10min_25_08.csv",
    "Gold_15min_25_08.csv",
    "Gold_30min_25_08.csv",
    "Gold_1h_25_08.csv",
    "Gold_4h_25_08.csv",
    "Gold_D_25_74.csv",
    "Gold_W_25_74.csv",
    "Gold_M_25_74.csv"
]
#how to connect with azure sample


# =====Example code setup ===
import streamlit as st
import pandas as pd
from io import BytesIO
from azure.storage.blob import BlobServiceClient
import config

st.set_page_config(layout="wide")
st.title("📊 Azure Blob Storage CSV Reader with Auto Loading")

try:
    # Connect to Azure Blob Storage
    st.info("🔌 Connecting to Azure Blob Storage...")
    blob_service_client = BlobServiceClient.from_connection_string(config.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(config.CONTAINER_NAME)
    st.success("✅ Connection to Azure successful.")
except Exception as e:
    st.error(f"❌ Failed to connect to Azure Blob Storage: {e}")
    st.stop()

st.markdown("---")

# List and read all CSV files in container
st.subheader("📁 Loading all `.csv` files from Azure Container")

loaded_any = False

for blob in container_client.list_blobs():
    if blob.name.endswith(".csv"):
        st.write(f"📂 Reading file: **{blob.name}**")
        try:
            blob_data = container_client.get_blob_client(blob.name).download_blob().readall()
            df = pd.read_csv(BytesIO(blob_data))
            st.success(f"✅ Loaded: {blob.name}")
            st.dataframe(df.head())
            loaded_any = True
        except Exception as e:
            st.error(f"❌ Failed to load {blob.name}: {e}")

if not loaded_any:
    st.warning("⚠️ No `.csv` files found in the container.")
