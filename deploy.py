import os
import sys
import shutil
from datetime import datetime


def deploy():
    todaysReleaseFolderPath = createTodaysReleaseFolder()
    # Creation of the release folder and sub folders : FE, BE, PROPS
    release_folder_path = createReleaseFolder(todaysReleaseFolderPath)
    bkp_folder_path = createBkpFolder(todaysReleaseFolderPath)
    release_folders_path = moveReleaseToNewlyCreatedFolder(release_folder_path)

    # Creation of the backup folder and sub folders : FE, BE, PROPS. Creates only the folders required according to deploy
    bkp_folders_path = createFoldersForBkpFolder(
        bkp_folder_path, release_folders_path)
    print(bkp_folders_path)

    # backup files
    deploy_paths = backupAppsDeployedAccordingToWhatIsBeingDeployed(
        bkp_folders_path)

    # Actual deploy
    deployFiles(release_folders_path, deploy_paths)


def createFolderNameWithDate():
    todays_date = getFormattedDate()
    folder_name = "/rel-" + todays_date
    return folder_name


def getFormattedDate():
    # Get the current date and time
    current_datetime = datetime.now()

    # Extract the date part from the datetime object
    current_date = current_datetime.date()

    # Format the date as "DDMMYYYY"
    formatted_date = current_datetime.strftime("%d%m%Y")
    return formatted_date


def createTodaysReleaseFolder():
    destination_folder_path = r'C:\Users\papab\Documents\Rilasci'
    release_folder_name_path = destination_folder_path + createFolderNameWithDate()
    folder_name = createFolderNameWithDate()

    # Check if the folder already exists
    if os.path.exists(release_folder_name_path):
        maxIndexFound = findAllExistingDeployFoldersWithTodaysDateAndReturnMax(
            destination_folder_path, folder_name)

        i = 1 if maxIndexFound is None else maxIndexFound + 1
        while True:
            new_folder_name = f"{folder_name}_{i}"
            if not os.path.exists(os.path.join(destination_folder_path, new_folder_name)):
                release_folder_name_path = destination_folder_path + new_folder_name
                break
            i += 1

    os.mkdir(release_folder_name_path)
    return release_folder_name_path


def findAllExistingDeployFoldersWithTodaysDateAndReturnMax(sourcePath, folderName):
    # Find all folders in the source path, where all releases are
    folder_in_path = os.listdir(sourcePath)

    # Remove the first character, remove'/'
    stripped_folder_name = folderName[1:]

    # Filter the results to only include directories that start with the specified prefix
    matching_folders = [item for item in folder_in_path if os.path.isdir(
        os.path.join(sourcePath, item)) and item.startswith(stripped_folder_name)]

    # Find the folder with the largest value
    largest_folder = max(matching_folders, key=lambda x: int(
        x.split("_")[-1]) if "_" in x else 0, default="")

    # Extract the numeric part from the folder name
    numeric_part = largest_folder.split(
        "_")[-1] if "_" in largest_folder else None

    return int(numeric_part) if numeric_part is not None else numeric_part


def createBkpFolder(path):
    bkp_folder_name = "/bkp"
    bkp_folder_path_name = path + bkp_folder_name
    os.mkdir(bkp_folder_path_name)
    return bkp_folder_path_name


def createFoldersForBkpFolder(bkpFolderPath, releaseFolderPaths):

    bpk_folders_path = {}
    if releaseFolderPaths.get('RELEASE_FE_FOLDER_PATH') is not None:
        os.mkdir(bkpFolderPath + "/FE")
        bpk_folders_path['BKP_FE_FOLDER_PATH'] = bkpFolderPath + "/FE"

    if releaseFolderPaths.get('RELEASE_BE_FOLDER_PATH') is not None:
        os.mkdir(bkpFolderPath + "/BE")
        bpk_folders_path['BKP_BE_FOLDER_PATH'] = bkpFolderPath + "/BE"

    if releaseFolderPaths.get('RELEASE_PROPS_FOLDER_PATH') is not None:
        os.mkdir(bkpFolderPath + "/PROPS")
        bpk_folders_path['BKP_PROPS_FOLDER_PATH'] = bkpFolderPath + "/PROPS"

    return bpk_folders_path


def createReleaseFolder(path):
    release_folder_name = "/release"
    release_folder_path_name = path + release_folder_name
    os.mkdir(release_folder_path_name)
    return release_folder_path_name


def moveReleaseToNewlyCreatedFolder(destinationFolderPath):
    try:
        desktopPath = os.path.expanduser("~/Desktop")
        folder_to_copy = "/rel"
        source_folder = desktopPath + folder_to_copy
        paths = {}
        if os.path.exists(source_folder):
            if (os.path.exists(source_folder + "/FE")):
                fe_path = moveFE(source_folder, destinationFolderPath)
                paths['RELEASE_FE_FOLDER_PATH'] = fe_path

            if (os.path.exists(source_folder + "/BE")):
                be_path = moveBE(source_folder, destinationFolderPath)
                paths['RELEASE_BE_FOLDER_PATH'] = be_path

            if (os.path.exists(source_folder + "/PROPS")):
                props_path = movePROPS(source_folder, destinationFolderPath)
                paths['RELEASE_PROPS_FOLDER_PATH'] = props_path

            os.rmdir(source_folder)
            return paths
        else:
            print("Could not initiate deploy, there is no folder on desktop, path:{}".format(
                source_folder))

            # Remove created folders if no rel folder is found on desktop
            stripped_directory_path = destinationFolderPath.rstrip("/release")
            shutil.rmtree(stripped_directory_path)
            # Stops the program completely
            sys.exit()

    except shutil.Error:
        print("A folder with the same name already exists")
        return


def moveFE(sourceFolder, destinationPath):
    folderToMovePath = sourceFolder + "/FE"
    try:
        movedFolderPath = shutil.move(folderToMovePath, destinationPath)
        return movedFolderPath
    except FileNotFoundError:
        print("Could not move FE folder, reason: folder not found")


def moveBE(sourceFolder, destinationPath):
    folderToMovePath = sourceFolder + "/BE"
    try:
        movedFolderPath = shutil.move(folderToMovePath, destinationPath)
        return movedFolderPath
    except FileNotFoundError:
        print("Could not move BE folder, reason: folder not found")


def movePROPS(sourceFolder, destinationPath):
    folderToMovePath = sourceFolder + "/PROPS"
    try:
        movedFolderPath = shutil.move(folderToMovePath, destinationPath)
        return movedFolderPath
    except FileNotFoundError:
        print("Could not move PROPS folder, reason: folder not found")


def backupAppsDeployedAccordingToWhatIsBeingDeployed(bkpFoldersPath):
    # FE
    deployPaths = {"FE_DEPLOY_PATH": r'C:\Users\papab\Documents\testCopy'}
    if bkpFoldersPath.get('BKP_FE_FOLDER_PATH') is not None:
        source_folder_path = r'C:\Users\papab\Documents\testCopy'
        move_action = "MOVE"
        copyOrMoveFilesToDestination(
            source_folder_path, bkpFoldersPath.get('BKP_FE_FOLDER_PATH'), move_action)

    return deployPaths


def deployFiles(releaseFoldersPath, deployPaths):
    if releaseFoldersPath.get('RELEASE_FE_FOLDER_PATH') is not None:
        source_folder_path = releaseFoldersPath.get('RELEASE_FE_FOLDER_PATH')
        copy_action = "COPY"
        copyOrMoveFilesToDestination(
            source_folder_path, deployPaths.get('FE_DEPLOY_PATH'), copy_action)


def copyOrMoveFilesToDestination(sourcePath, destinationPath, action):
    # Get a list of all files in the source folder
    files = os.listdir(sourcePath)
    # Copy each file from the source folder to the destination folder
    for file in files:
        source_file_path = os.path.join(sourcePath, file)
        print(source_file_path)
        destination_file_path = os.path.join(destinationPath, file)
        print(destination_file_path)
        if action == "COPY":
            shutil.copy2(source_file_path, destination_file_path)
            print(f"Moving '{file}' to '{destinationPath}'")
        else:
            shutil.move(source_file_path, destination_file_path)
            print(f"Copying '{file}' to '{destinationPath}'")


deploy()
