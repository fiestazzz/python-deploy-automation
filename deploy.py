import os
import shutil
from datetime import datetime


def deploy():
    # moved_folder_path = moveFolderToReleases()

    todaysReleaseFolderPath = createTodaysReleaseFolder()
    bkp_folder_path = createBkpFolder(todaysReleaseFolderPath)
    bkp_folder_path = createFoldersForBkpFolder(bkp_folder_path)
    release_folder_path = createReleaseFolder(todaysReleaseFolderPath)
    moveReleaseToNewlyCreatedFolder(release_folder_path)


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
    os.mkdir(release_folder_name_path)
    return release_folder_name_path


def createBkpFolder(path):
    bkp_folder_name = "/bkp"
    bkp_folder_path_name = path + bkp_folder_name
    os.mkdir(bkp_folder_path_name)
    return bkp_folder_path_name


def createFoldersForBkpFolder(bkpFolderPath):
    bkp_FE_folder_path = os.mkdir(bkpFolderPath + "/FE")
    bkp_BE_folder_path = os.mkdir(bkpFolderPath + "/BE")
    bkp_PROPS_folder_path = os.mkdir(bkpFolderPath + "/PROPS")
    paths = {"BKP_FE_FOLDER_PATH": bkp_FE_folder_path,
             "BKP_BE_FOLDER_PATH": bkp_BE_folder_path, "BKP_PROPS_FOLDER_PATH": bkp_PROPS_folder_path}
    return paths


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
        fe_path = moveFE(source_folder, destinationFolderPath)
        be_path = moveBE(source_folder, destinationFolderPath)
        props_path = movePROPS(source_folder, destinationFolderPath)
        paths = {"RELEASE_FE_FOLDER_PATH": fe_path,
                 "RELEASE_BE_FOLDER_PATH": be_path, "RELEASE_PROPS_FOLDER_PATH": props_path}
        os.rmdir(source_folder)
        return paths
    except shutil.Error:
        print("A folder with the same name already exists")
        return


def moveFE(sourceFolder, destinationPath):
    folderToMovePath = sourceFolder + "/FE"
    try:
        movedFolderPath = shutil.move(folderToMovePath, destinationPath)
        return movedFolderPath
    except FileNotFoundError:
        print("Error while trying to move FE folder, reason: folder not found")


def moveBE(sourceFolder, destinationPath):
    folderToMovePath = sourceFolder + "/BE"
    try:
        movedFolderPath = shutil.move(folderToMovePath, destinationPath)
        return movedFolderPath
    except FileNotFoundError:
        print("Error while trying to move BE folder, reason: folder not found")


def movePROPS(sourceFolder, destinationPath):
    folderToMovePath = sourceFolder + "/PROPS"
    try:
        movedFolderPath = shutil.move(folderToMovePath, destinationPath)
        return movedFolderPath
    except FileNotFoundError:
        print("Error while trying to move PROPS folder, reason: folder not found")


deploy()
