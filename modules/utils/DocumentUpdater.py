import os
import requests
import shutil

class DocumentUpdater:
    """
    A class for updating document files from AWS github documentation repo or a local source folder.

    This class provides methods for downloading and updating document files either from
    the official AWS documentation repository or from a local source folder, which can
    be used for mocking AWS documentation updates.

    Methods:
        download_file(url, local_path):
            Downloads a file from a given URL and saves it locally.

        get_changed_files(owner, repo_name, base_commit, head_commit):
            Retrieves the list of changed files between two commits in a GitHub repository.

        download_changed_files_in_subfolder(owner, repo_name, branch, local_directory, subfolder, base_commit):
            Downloads changed files within a specified subfolder of a GitHub repository.

        get_last_commit_id(owner, repo_name, branch):
            Retrieves the last commit ID of a specified branch in a GitHub repository.

        update_document_files_from_awsdocs(knowledge_base):
            Updates document files from the AWS documentation github repository.

        update_document_files_from_awsdocs_mock(knowledge_base):
            Updates document files from a local source folder (mocking AWS documentation).
    """

    def __init__(self):
        pass
 
    def download_file(self, url, local_path):
        """
        Downloads a file from the specified URL and saves it locally.

        Parameters:
            url (str): The URL of the file to be downloaded.
            local_path (str): The local path where the file should be saved.

        Returns:
            None
        """
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
                print(f"Downloaded: {local_path}")
        else:
            print(f"Failed to download: {local_path}")

    def get_changed_files(self, owner, repo_name, base_commit, head_commit):
        """
        Retrieves the list of changed files between two commits in a GitHub repository.

        Parameters:
            owner (str): The owner of the GitHub repository.
            repo_name (str): The name of the GitHub repository.
            base_commit (str): The base commit to compare.
            head_commit (str): The head commit to compare.

        Returns:
            list: A list of filenames that have changed between the specified commits.
        """
        url = f"https://api.github.com/repos/{owner}/{repo_name}/compare/{base_commit}...{head_commit}"
        response = requests.get(url)
        if response.status_code == 200:
            comparison_data = response.json()
            changed_files = comparison_data.get("files", [])
            return [file["filename"] for file in changed_files]
        else:
            print("Failed to fetch changed files.")
            return []

    def download_changed_files_in_subfolder(self, owner, repo_name, branch, local_directory, subfolder, base_commit):
        """
        Downloads changed files within a specified subfolder of a GitHub repository.

        Parameters:
            owner (str): The owner of the GitHub repository.
            repo_name (str): The name of the GitHub repository.
            branch (str): The branch from which to fetch changes.
            local_directory (str): The local directory where files will be saved.
            subfolder (str): The subfolder within the repository to filter changes.
            base_commit (str): The base commit to compare for changes.

        Returns:
            None
        """
        print(f'fetching file changes in {repo_name} github repo since commit {base_commit}')
        head_commit = f"{owner}:{branch}"

        # Get the list of changed files between the base and head commits
        changed_files = self.get_changed_files(owner, repo_name, base_commit, head_commit)

        for file_path in changed_files:
            # Check if the file is within the specified subfolder
            if file_path.startswith(subfolder):
                # Build the raw file URL
                raw_file_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/{file_path}"
                # Build the local file path
                file_path=file_path.replace(subfolder+'/', '')
                local_file_path = os.path.join(local_directory, file_path)
                # Create the local directory if it doesn't exist
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                # Download the file
                self.download_file(raw_file_url, local_file_path)

    def get_last_commit_id(self, owner, repo_name, branch):
        """
        Retrieves the last commit ID of a specified branch in a GitHub repository.

        Parameters:
            owner (str): The owner of the GitHub repository.
            repo_name (str): The name of the GitHub repository.
            branch (str): The branch for which to fetch the last commit ID.

        Returns:
            str: The last commit ID of the specified branch.
        """
        url = f"https://api.github.com/repos/{owner}/{repo_name}/git/ref/heads/{branch}"
        response = requests.get(url)
        if response.status_code == 200:
            ref_data = response.json()
            return ref_data.get("object", {}).get("sha", "")
        else:
            print(f"Failed to fetch last commit ID for branch: {branch}")
            return ""
    
    def update_document_files_from_awsdocs(self, knowledge_base:str):
        """
        Updates document files from the AWS github documentation repository.

        Parameters:
            knowledge_base (str): The name of the AWS github documentation repository.

        Returns:
            None
        """
        owner = "awsdocs"
        repo_name = knowledge_base
        branch = "main"
        subfolder = "doc_source"
        local_directory = "Documents/amazon-sagemaker-developer-guide"
        with open("modules/utils/lastFetched-"+repo_name, 'r') as file:
            base_commit = file.readline()
        self.download_changed_files_in_subfolder(owner, repo_name, branch, local_directory, subfolder, base_commit)
        with open("modules/utils/lastFetched-"+repo_name, 'w') as file:
            file.write(self.get_last_commit_id(owner, repo_name, branch))

    def update_document_files_from_awsdocs_mock(self, knowledge_base):
        """
        Updates document files from a local source folder (Assesment, mocking AWS documentation).

        Parameters:
            knowledge_base (str): The path of the raw knowledge base.

        Returns:
            None
        """
        source_folder = os.path.join("Assesment", knowledge_base)
        destination_folder = os.path.join("Documents", knowledge_base)
        files_to_move = os.listdir(source_folder)
        for file_name in files_to_move:
            source_file_path = os.path.join(source_folder, file_name)
            destination_file_path = os.path.join(destination_folder, file_name)
            if os.path.isfile(source_file_path):
                shutil.copy2(source_file_path, destination_file_path)

documentUpdater=DocumentUpdater()

if __name__ == "__main__":
    documentUpdater.update_document_files_from_awsdocs(knowledge_base = "amazon-sagemaker-developer-guide")
    documentUpdater.update_document_files_from_awsdocs_mock(knowledge_base = "sagemaker_documentation")
