from azure.storage.filedatalake import DataLakeServiceClient
import os

class ADLSUploader:
    def __init__(self, account_name, account_key, container_name, local_batch_folder, local_real_time_folder, adls_root_folder):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.local_batch_folder = local_batch_folder
        self.local_real_time_folder = local_real_time_folder
        self.adls_root_folder = adls_root_folder
        self.adls_client = self.initialize_adls_client()

    def initialize_adls_client(self):
        from azure.storage.filedatalake import DataLakeServiceClient
        adls_url = f"https://{self.account_name}.dfs.core.windows.net"
        return DataLakeServiceClient(account_url=adls_url, credential=self.account_key)

    def upload_data(self, location, data_type):
        """
        Uploads data to ADLS based on the data type (batch or real-time).
        """
        folder = self.local_batch_folder if data_type == "batch" else self.local_real_time_folder
        location_folder = os.path.join(self.adls_root_folder, data_type, location)  # Base folder for the location

        # Define subfolders based on data type
        if data_type == "batch":
            consumption_data_folder = os.path.join(location_folder, "consumption_batch_data")
            production_data_folder = os.path.join(location_folder, "production_batch_data")
        elif data_type == "real-time":
            consumption_data_folder = os.path.join(location_folder, "energy_consumption")
            production_data_folder = os.path.join(location_folder, "production_simulation")

        # Recursively upload files for the given location and data type
        for root, dirs, files in os.walk(os.path.join(folder, location)):
            for file in files:
                local_file_path = os.path.join(root, file)  # Full path to the local file
                file_name = os.path.basename(file)  # Extract only the file name

                # Determine where the file belongs: to consumption_data or production_data
                if 'consumption' in file_name.lower():
                    adls_file_path = os.path.join(consumption_data_folder, file_name)
                elif 'production' in file_name.lower():
                    adls_file_path = os.path.join(production_data_folder, file_name)
                else:
                    continue  # Skip files that don't match the pattern

                # Upload file to ADLS
                self.upload_to_adls(local_file_path, adls_file_path)

    def upload_to_adls(self, local_file_path, adls_file_path):
        """
        Handles the actual upload of a file to ADLS.
        """
        file_system_client = self.adls_client.get_file_system_client(self.container_name)

        # Ensure the directory structure exists in ADLS
        directory_path = os.path.dirname(adls_file_path)
        directory_client = file_system_client.get_directory_client(directory_path)
        try:
            directory_client.create_directory()
        except Exception:
            pass  # Ignore if the directory already exists

        # Get the file client for the actual file
        file_client = file_system_client.get_file_client(adls_file_path)

        # Upload the file
        with open(local_file_path, "rb") as file_data:
            file_client.create_file()
            file_client.append_data(file_data, offset=0, length=os.path.getsize(local_file_path))
            file_client.flush_data(os.path.getsize(local_file_path))

        print(f"Uploaded {local_file_path} to ADLS as {adls_file_path}")

    def upload_based_on_keyword(self, locations, keyword):
        """
        Uploads either batch or real-time data based on the keyword passed.
        """
        if keyword.lower() not in ["batch", "real-time"]:
            raise ValueError("Keyword must be either 'batch' or 'real-time'.")

        for location in locations:
            print(f"Uploading {keyword} data for location: {location}")
            self.upload_data(location, keyword)
            
            
if __name__ == "__main__":
    account_name = "<storage_name>"
    account_key = "<storage_key>"
    container_name = "<container_name>"
    local_batch_folder = "batch-output"
    local_real_time_folder = "realtime-output"
    adls_root_folder = "data"

    # Initialize the uploader
    uploader = ADLSUploader(account_name, account_key, container_name, local_batch_folder, local_real_time_folder, adls_root_folder)

    # Define locations and keyword
    locations = ["Boston", "New York", "San Francisco", "Chicago"]
    keyword = "batch"  # Change to "real-time" for real-time data uploads

    # Upload data based on the keyword
    uploader.upload_based_on_keyword(locations, keyword)

    print("Upload complete.")



