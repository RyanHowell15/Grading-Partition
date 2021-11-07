"""
Script to interact with google sheets.
Requires gspread and oauth downloaded.

author: Ryan Howell
"""
import gspread
from gspread.models import Cell
from oauth2client.service_account import ServiceAccountCredentials

def Create_Sheet(partition, settings):
    #Authorize the API
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]
    file_name = 'client_key.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
    client = gspread.authorize(creds)

    #Fetch the sheet
    ss = client.open_by_url(settings["sheetUrl"])
    wksheet = ss.add_worksheet(title="New Assignment", rows = 100, cols = 26)

    sheetId = wksheet._properties['sheetId']

    FormatSheet(ss, sheetId, partition)

    WriteData(ss, wksheet, partition)

def WriteData(spreadsheet, wksheet, partition):
    cells = []

    instructorsPerRow = 4
    colsPerInstructor = 4

    maxPartitionLength = 0
    currRow = 1
    currCol = 2
    for instructorNum, i in enumerate(sorted(partition.keys())):
        if instructorNum != 0 and instructorNum % instructorsPerRow == 0: #starting a new row
            #advance row by the length of the longest partition
            currRow += maxPartitionLength + 4
            maxPartitionLength = 0
            currCol = 2

        #write instructor name
        cells.append(Cell(row = currRow, col = currCol, value = i))

        #write students
        oldRow = currRow
        for submission in partition[i]:
            currRow+=1
            cells.append(Cell(row = currRow, col = currCol, value = submission[0]))

            if len(submission) > 1:
                cells.append(Cell(row = currRow, col = currCol + 1, value = submission[1]))

        currRow=oldRow

        partitionLength = len(partition[i])
        maxPartitionLength = max(maxPartitionLength, partitionLength)
        currCol += colsPerInstructor
    wksheet.update_cells(cells)

def FormatSheet(spreadsheet, sheetId, partition):
    requests = []

    instructorsPerRow = 4
    colsPerInstructor = 4
    #lastColum should not be more than 25
    lastColum = instructorsPerRow * colsPerInstructor

    startRow = 0
    endRow = 1
    startCol = 1
    endCol = 3
    maxPartitionLength = 0
    for instructorNum, i in enumerate(sorted(partition.keys())):
        if instructorNum != 0 and instructorNum % instructorsPerRow == 0: #starting a new row
            #advance row by the length of the longest partition
            rowAdvance = maxPartitionLength + 4
            startRow += rowAdvance
            endRow += rowAdvance
            maxPartitionLength = 0

            #create long border above instructor names
            requests.append(TopBorder(Range(sheetId, startRow, endRow, 0, lastColum)))

            #reset column count
            startCol = 1
            endCol = 3

        requests.append(Merge(Range(sheetId, startRow, endRow, startCol, endCol)))

        # create border below instructor name
        # +1 to row numbers because we this is techinally a bottom border
        requests.append(TopBorder(Range(sheetId, startRow + 1, endRow + 1, startCol, endCol)))

        partitionLength = len(partition[i])
        maxPartitionLength = max(maxPartitionLength, partitionLength)
        startCol += colsPerInstructor
        endCol += colsPerInstructor
        
    #increase column widths
    for i in range(1, lastColum, colsPerInstructor):
        requests.append(ChangeWidth(DimensionRange(sheetId, "COLUMNS", i, i+2), 250))

    body = {
        "requests": requests
    }
    return spreadsheet.batch_update(body)
    

def TopBorder(range, style="SOLID_MEDIUM"):
    """
    Creates a border update request. Top border only
    https://developers.google.com/sheets/api/samples/formatting

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#UpdateBordersRequest

    Args:
        range ([type]): [description]
        style (str, optional): [description]. Defaults to "SOLID_MEDIUM".

    Returns:
        [type]: [description]
    """
    return {
        "updateBorders": {
            "range": range,
            "top": {
                "style": style,
            }
        }
    }


def Merge(range, mergeType="MERGE_ALL"):
    """
    Returns a Google Sheets API formatted MergeCell request

    Args:
        range ([type]): [description]
        mergeType (str, optional): [description]. Defaults to "MERGE_ALL".

    Returns:
        [type]: [description]
    """
    return {
        "mergeCells": {
            "mergeType": mergeType,
            "range": range
        }
    }


def Range(sheetId, startRow, endRow, startCol, endCol):
    """
    Returns a Google Sheets API formatted GridRange

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#GridRange

    Args:
        sheetId ([type]): [description]
        startRow ([type]): [description]
        endRow ([type]): [description]
        startCol ([type]): [description]
        endCol ([type]): [description]

    Returns:
        [type]: [description]
    """
    return {
        "sheetId": sheetId,
        "startRowIndex": startRow,
        "endRowIndex": endRow,
        "startColumnIndex": startCol,
        "endColumnIndex": endCol
    }


def DimensionRange(sheetId, dimension, startIndex, endIndex):
    """
    https://developers.google.com/sheets/api/reference/rest/v4/DimensionRange

    Args:
        sheetId ([type]): [description]
        dimension ([type]): [description]
        startIndex ([type]): [description]
        endIndex ([type]): [description]

    Returns:
        [type]: [description]
    """
    return {
        "sheetId": sheetId,
        "dimension": dimension,
        "startIndex": startIndex,
        "endIndex": endIndex
    }


def ChangeWidth(range, pixelSize):
    """
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#updatedimensionpropertiesrequest

    Args:
        range ([type]): [description]
        pixelSize ([type]): [description]

    Returns:
        [type]: [description]
    """
    return {
        "updateDimensionProperties": {
            "range": range,
            "properties": {
                "pixelSize": pixelSize
            },
            "fields": "pixelSize"
        }
    }
