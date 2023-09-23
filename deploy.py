import os
import shutil
from datetime import datetime


def deploy():
    # moved_folder_path = moveFolderToReleases()

    todaysReleaseFolderPath = createTodaysReleaseFolder()
    bkp_folder_path = createBkpFolder(todaysReleaseFolderPath)
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


def createReleaseFolder(path):
    release_folder_name = "/release"
    release_folder_path_name = path + release_folder_name
    os.mkdir(release_folder_path_name)
    return release_folder_path_name


def moveReleaseToNewlyCreatedFolder(destinationFolderPath):
    try:
        desktopPath = os.path.expanduser("~/Desktop")
        folder_to_cut = "/rel"
        source_folder = desktopPath + folder_to_cut
        fe_path = moveFE(source_folder, destinationFolderPath)
        be_path = moveBE(source_folder, destinationFolderPath)
        os.rmdir(source_folder)
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


deploy()
