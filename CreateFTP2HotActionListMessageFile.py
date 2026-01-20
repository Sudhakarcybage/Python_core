#
# This script creates test message files for FTP2 Day2 delivery.
# This is yet another version of hot/action list creation, this one
# takes most configuration options from the command line. Thus allow
# it to be used in other scripts.
#
from CommonFileUtilities import *
import sys
import os
import shutil

MAX_RECORDS_PER_DATAFRAME = 15

USAGE_STRING = \
"USAGE: python CreateFTP2HotActionListMessageFile.py FTP2_Folder \"hot\"|\"action\" destinationISAMID ListId ListSizeKB destinationFolder\n" \
"Where\n" \
"                      FTP2_Folder        is the root of FTP2, i.e. C:\\Git_RepoStorage\\FTP2\n" \
"                      \"hot\"|\"action\"     request hot or action list.\n" \
"                      destinationISAMID  recipient and destination address, e.g. 00580000\n" \
"                      ListId             hot or action list ID.\n" \
"                      ListSizeKB         list size in 1000's of bytes.\n" \
"                      destinationFolder  destination folder for generated message files.\n" \
"\n" \
"Example:\n" \
"    CreateFTP2HotActionListMessageFile.py C:\\Git_RepoStorage\\FTP2 action 00580000 1 10000 E:\\Jobs\\ItsoServerSimulator1_1_1\\FromHops\n" \
"Notes:\n" \
"  The script requires two tools to have been built, ITSO_XML_Resealer and MakeITSOTable, these\n" \
"  can both be built using ITSOBuildAll.py.\n"

#
# Place Holders may appear in strings and are replaced by
# their values.
#
DESTINTATION_PLACE_HOLDER = "$DESTINATION$"
MESSAGE_CODE_PLACE_HOLDER = "$MESSAGE_CODE$"
PLACE_HOLDER_DICTIONARY = { DESTINTATION_PLACE_HOLDER : "00600056",  MESSAGE_CODE_PLACE_HOLDER : "0602" }

MAKE_ITSO_TABLE_EXE_RELATIVE = "\\ITSO_Tools\\ITSOTest\\TestTools\\Tables\\MakeITSOTable\\Debug\\MakeITSOTable.exe"
ITSO_XML_RESEALER_EXE_RELATIVE = "\\ITSO_Tools\\ITSOTest\\TestTools\\ITSO_XMLResealer\\Debug\\ITSO_XMLResealer.exe"

#
# Fixed strings
#

#
# Hot list record has two string to format within it the ISSN and the hot list ID.
#
HOT_LIST_RECORD_TEMPLATE =    '0,0,01,0047,%07X,9,000D,01,0202,01,%04X,01,02,01,0011,0001,'

#
# Unblock Shell
#
ACTION_LIST_RECORD_TEMPLATE = '0,1,01,0047,%07X,9,000C,02,0204,01,%04X,06,01,0011,0001,'
#                              ^ ^ ^  ^     ^   ^ ^    ^  ^    ^  ^    ^  ^  ^    ^
#                              | | |  |     |   | |    |  |    |  |    |  |  |    |
#                              | | |  |     |   | |    |  |    |  |    |  |  |    |...OriginalActtionListIdentifier
#                              | | |  |     |   | |    |  |    |  |    |  |  |...ActionListOriginator
#                              | | |  |     |   | |    |  |    |  |    |  |...ActionSequenceNumber
#                              | | |  |     |   | |    |  |    |  |    |...ActionToTake 6 = (unhot list shell)
#                              | | |  |     |   | |    |  |    |  |...ActionListID
#                              | | |  |     |   | |    |  |    |...RecordVersionNumber
#                              | | |  |     |   | |    |  |...Bitmap
#                              | | |  |     |   | |    |...RecordType 2 = actionlist
#                              | | |  |     |   | |...RecordLength
#                              | | |  |     |   |...ISRN_CHD
#                              | | |  |     |...ISRN_ISSN
#                              | | |  |...ISRN_OID
#                              | | |...IIN_Index
#                              | |...INS#
#                              |...KeyType
#
#
#
#
#
#
#
#


DUMMY_HASH = "1111222233334444555566667777888899990000"

MESSAGE_HEADER = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n" \
"<!DOCTYPE ITSO_HOPS_to_POST_File [<!ELEMENT ITSO_HOPS_to_POST_File (ITSO_Message_Header, ITSO_Message_Frame)>\n" \
"<!ELEMENT ITSO_Message_Header (ITSO_Message_Version, ITSO_Message_Class)>\n" \
"<!ELEMENT ITSO_Message_Frame (ITSO_Batch_Header, ITSO_Message_Body)>\n" \
"<!ELEMENT ITSO_Batch_Header (ITSO_Message_CRC, ITSO_Originator, ITSO_Recipient,(ITSO_Recipient_Type | (ITSO_Recipient_Type, ITSO_Group_Message_Seq_Num,ITSO_ISAM_Message_Seq_Num))?)>\n" \
"<!ELEMENT ITSO_Message_Body (ITSO_Data_Frame | ITSO_Secure_Data_Frame)+>\n" \
"<!ELEMENT ITSO_Data_Frame (ITSO_Message_Code, ITSO_DTS, ITSO_Data_Block, ITSO_DF_Trailer)>\n" \
"<!ELEMENT ITSO_Data_Block (ITSO_DB_Len, ITSO_Num_Data_Elements, ITSO_Dest_Count, ITSO_Destination, ITSO_Data)>\n" \
"<!ELEMENT ITSO_DF_Trailer (ITSO_Trailer_Length, ITSO_KID, ITSO_SealerID, ITSO_Seq_Num, ITSO_Seal)>\n" \
"<!ELEMENT ITSO_Data (#PCDATA)>\n" \
"<!ELEMENT ITSO_DB_Len (#PCDATA)>\n" \
"<!ELEMENT ITSO_Dest_Count (#PCDATA)>\n" \
"<!ELEMENT ITSO_Destination (#PCDATA)>\n" \
"<!ELEMENT ITSO_DTS (#PCDATA)>\n" \
"<!ELEMENT ITSO_KID (#PCDATA)>\n" \
"<!ELEMENT ITSO_Message_Class (#PCDATA)>\n" \
"<!ELEMENT ITSO_Message_Code (#PCDATA)>\n" \
"<!ELEMENT ITSO_Message_CRC (#PCDATA)>\n" \
"<!ELEMENT ITSO_Message_Version (#PCDATA)>\n" \
"<!ELEMENT ITSO_Num_Data_Elements (#PCDATA)>\n" \
"<!ELEMENT ITSO_Originator (#PCDATA)>\n" \
"<!ELEMENT ITSO_Recipient (#PCDATA)>\n" \
"<!ELEMENT ITSO_Recipient_Type (#PCDATA)>\n" \
"<!ELEMENT ITSO_Group_Message_Seq_Num (#PCDATA)>\n" \
"<!ELEMENT ITSO_ISAM_Message_Seq_Num (#PCDATA)>\n" \
"<!ELEMENT ITSO_SDF (#PCDATA)>\n" \
"<!ELEMENT ITSO_Seal (#PCDATA)>\n" \
"<!ELEMENT ITSO_SealerID (#PCDATA)>\n" \
"<!ELEMENT ITSO_Secure_Data_Frame (ITSO_SDF)>\n" \
"<!ELEMENT ITSO_Seq_Num (#PCDATA)>\n" \
"<!ELEMENT ITSO_Trailer_Length (#PCDATA)>]>\n" \
"<ITSO_HOPS_to_POST_File>\n" \
"<ITSO_Message_Header>\n" \
"<ITSO_Message_Version>3</ITSO_Message_Version>\n" \
"<ITSO_Message_Class>2</ITSO_Message_Class>\n" \
"</ITSO_Message_Header>\n" \
"<ITSO_Message_Frame>\n" \
"<ITSO_Batch_Header>\n" \
"<ITSO_Message_CRC>6A32</ITSO_Message_CRC>\n" \
"<ITSO_Originator>6335970060004E</ITSO_Originator>\n" \
"<ITSO_Recipient>633597$DESTINATION$</ITSO_Recipient>\n" \
"<ITSO_Recipient_Type>00</ITSO_Recipient_Type>\n" \
"</ITSO_Batch_Header>\n" \
"<ITSO_Message_Body>\n"

MESSAGE_FOOTER = \
"</ITSO_Message_Body>\n" \
"</ITSO_Message_Frame>\n" \
"</ITSO_HOPS_to_POST_File>\n"

DATA_FRAME_HEADER =  \
"<ITSO_Data_Frame>\n" \
"<ITSO_Message_Code>$MESSAGE_CODE$</ITSO_Message_Code>\n" \
"<ITSO_DTS>635395</ITSO_DTS>\n" \
"<ITSO_Data_Block>\n"

DATA_FRAME_TRAILER = \
"</ITSO_Data_Block>\n" \
"<ITSO_DF_Trailer>\n" \
"<ITSO_Trailer_Length>14</ITSO_Trailer_Length>\n" \
"<ITSO_KID>50</ITSO_KID>\n" \
"<ITSO_SealerID>63359700600046</ITSO_SealerID>\n" \
"<ITSO_Seq_Num>00002F</ITSO_Seq_Num>\n" \
"<ITSO_Seal>5EA15EA15EA15EA1</ITSO_Seal>\n" \
"</ITSO_DF_Trailer>\n" \
"</ITSO_Data_Frame>\n"

OVERRIDE_NUMBER_RECORDS = 0

# Base ISSN make sure that the hot list create ISSN which are unlikely to exist.
BASE_ISSN = 8000000

def MakeITSOTableFullPath(ftp2Folder):
    name = ftp2Folder + MAKE_ITSO_TABLE_EXE_RELATIVE
    return name

def ITSOXMLResealerFullPath(ftp2Folder):
    return ftp2Folder + ITSO_XML_RESEALER_EXE_RELATIVE


def ReplacePlaceHolders(string):
    for placeHolder in PLACE_HOLDER_DICTIONARY.keys():
        string = string.replace(placeHolder, PLACE_HOLDER_DICTIONARY[placeHolder] )
    return string

def InsertStringWithPlaceHolders(outputFile, string):
    string = ReplacePlaceHolders(string)
    outputFile.writelines(string)

def CalculateRecordSize(recordTemplate):
    exampleRecord = recordTemplate % (1, 0xADAD)
    #strip comma
    exampleRecord = exampleRecord.replace(",", "")
    recordSize = len(exampleRecord) / 2
    return recordSize

def  CalculateNumberOfElement(recordTemplate):
    exampleRecord = recordTemplate % (1, 0xADAD)
    numberOfElements = exampleRecord.count(",")
    return numberOfElements

def StripTrailingComma(recordTemplate):
    return recordTemplate.rstrip(",")

def CreateSingleRecordDataFrame(outputFile, recordTemplate, ISSN, listID):

    InsertStringWithPlaceHolders(outputFile, DATA_FRAME_HEADER)

    recordSize = int(CalculateRecordSize(recordTemplate))
    numberOfElements = CalculateNumberOfElement(recordTemplate)
    recordTemplate = StripTrailingComma(recordTemplate)

    outputFile.write('<ITSO_DB_Len>%04X</ITSO_DB_Len>\n' % (2 + 1 + 1 + 7 + recordSize))
    outputFile.write('\n<ITSO_Num_Data_Elements>%02X</ITSO_Num_Data_Elements>\n' % (numberOfElements))
    outputFile.write('<ITSO_Dest_Count>01</ITSO_Dest_Count>\n')
    outputFile.write('<ITSO_Destination>633597%s</ITSO_Destination>\n' % (PLACE_HOLDER_DICTIONARY [DESTINTATION_PLACE_HOLDER ]))
    outputFile.write('<ITSO_Data>')
    outputFile.write(recordTemplate % (ISSN, listID))
    outputFile.write('</ITSO_Data>\n' )

    InsertStringWithPlaceHolders(outputFile, DATA_FRAME_TRAILER)

# def CreateSingleList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename):
#
#     f = open(outputFilename, "w")
#     InsertStringWithPlaceHolders(f, MESSAGE_HEADER)
#
#     recordNumber = 0
#     for recordNumber in range (0, numberRecords):
#         CreateSingleRecordDataFrame(f, recordTemplate, recordNumber + BASE_ISSN, listID)
#
#     InsertStringWithPlaceHolders(f, MESSAGE_FOOTER)
#
#     f.close()
def CreateSingleList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename, no_commas=False):
    f = open(outputFilename, "w")
    InsertStringWithPlaceHolders(f, MESSAGE_HEADER)

    for recordNumber in range(numberRecords):
        template = recordTemplate
        if no_commas:
            template = template.replace(",", "")
        CreateSingleRecordDataFrame(f, template, recordNumber + BASE_ISSN, listID)

    InsertStringWithPlaceHolders(f, MESSAGE_FOOTER)
    f.close()

def CreateMultiRecordDataFrameHeader(outputFile, recordTemplate, commas, recordsInFrame):
    InsertStringWithPlaceHolders(outputFile, DATA_FRAME_HEADER)

    recordSize = CalculateRecordSize(recordTemplate)
    numberOfElements = CalculateNumberOfElement(recordTemplate)

    outputFile.write('<ITSO_DB_Len>%08X14</ITSO_DB_Len>\n' % int(5 + 1 + 1 + 7 + 3 + (recordsInFrame * recordSize) + 20))

    if commas == True:
        numberDataElements = (recordsInFrame * numberOfElements) +1
    else:
        #numberDataElements = 1
        numberDataElements = 0  # No comma separation

    outputFile.write('\n<ITSO_Num_Data_Elements>%02X</ITSO_Num_Data_Elements>\n' % numberDataElements)

    outputFile.write('<ITSO_Dest_Count>01</ITSO_Dest_Count>\n')
    outputFile.write('<ITSO_Destination>633597%s</ITSO_Destination>\n' % (PLACE_HOLDER_DICTIONARY [DESTINTATION_PLACE_HOLDER ]))
    if OVERRIDE_NUMBER_RECORDS:
        outputFile.write('<ITSO_Data>%06X' % (OVERRIDE_NUMBER_RECORDS))
    else:
        outputFile.write('<ITSO_Data>%06X' % int(recordsInFrame))

    if commas:
        outputFile.write(',')

def CreateMultiRecordDataFrameTrailer(outputFile):

    outputFile.write('%s</ITSO_Data>\n' % (DUMMY_HASH))
    InsertStringWithPlaceHolders(outputFile, DATA_FRAME_TRAILER)

def CreateMultiRecordDataFrame(outputFile, recordTemplate, commas, firstISSN, recordsInFrame, listID):

    CreateMultiRecordDataFrameHeader(outputFile, recordTemplate, commas, recordsInFrame)

    for i in range (0, int(recordsInFrame)):
        record = recordTemplate % (firstISSN + i, listID)
        if commas == False:
            record = record.replace(",", "")
        outputFile.write("%s" % (record))

    CreateMultiRecordDataFrameTrailer(outputFile)


# def CreateMultiList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename):
#
#
#     f = open(outputFilename, "w")
#     InsertStringWithPlaceHolders(f, MESSAGE_HEADER)
#
#     numberDataFrames = (numberRecords + MAX_RECORDS_PER_DATAFRAME - 1)// MAX_RECORDS_PER_DATAFRAME
#
#     recordNumber = 0
#     for frameNumber in range (0, numberDataFrames):
#
#         recordsInFrame = numberRecords - (frameNumber * MAX_RECORDS_PER_DATAFRAME)
#         if recordsInFrame > MAX_RECORDS_PER_DATAFRAME:
#             recordsInFrame = MAX_RECORDS_PER_DATAFRAME
#
#         INSERT_COMMAS = True
#         CreateMultiRecordDataFrame(f, recordTemplate, INSERT_COMMAS, recordNumber + BASE_ISSN, recordsInFrame, listID)
#
#         recordNumber = recordNumber + recordsInFrame
#
#     InsertStringWithPlaceHolders(f, MESSAGE_FOOTER)
#     f.close()
def CreateMultiList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename, no_commas=False):
    f = open(outputFilename, "w")
    InsertStringWithPlaceHolders(f, MESSAGE_HEADER)

    numberDataFrames = (numberRecords + MAX_RECORDS_PER_DATAFRAME - 1)// MAX_RECORDS_PER_DATAFRAME

    recordNumber = 0
    for frameNumber in range(numberDataFrames):
        recordsInFrame = min(numberRecords - (frameNumber * MAX_RECORDS_PER_DATAFRAME), MAX_RECORDS_PER_DATAFRAME)
        INSERT_COMMAS = not no_commas
        CreateMultiRecordDataFrame(f, recordTemplate, INSERT_COMMAS, recordNumber + BASE_ISSN, recordsInFrame, listID)
        recordNumber += recordsInFrame

    InsertStringWithPlaceHolders(f, MESSAGE_FOOTER)
    f.close()

def CreateNoCommasList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename):


    f = open(outputFilename, "w")
    InsertStringWithPlaceHolders(f, MESSAGE_HEADER)

    INSERT_COMMAS = False
    recordNumber = 0
    CreateMultiRecordDataFrame(f, recordTemplate, INSERT_COMMAS, recordNumber + BASE_ISSN, numberRecords, listID)

    InsertStringWithPlaceHolders(f, MESSAGE_FOOTER)
    f.close()

def DetermineMessageCode(listType, format):
    messageCode = ""
    if format.lower() == "multi" or format.lower() == "nocommas":
        messageCode = "06"
    elif format.lower() == "single":
        messageCode = "0C"

    if len(messageCode) == 2:
        if listType.lower() == "hot":
            messageCode = messageCode + "02"
        elif listType.lower() == "action":
            messageCode = messageCode + "03"
        else:
            messageCode = ""

    return messageCode


def CheckDestinationISAM(destinationISAM):
    result = True
    if len(destinationISAM) != 8:
        print ("destinationISAM wrong size (should be 8) %s" % (destinationISAM))
        result = False

    return result

def GetRecordTemplate(listType):
    if listType.lower() == "hot":
        recordTemplate = HOT_LIST_RECORD_TEMPLATE
    elif listType.lower() == "action":
        recordTemplate = ACTION_LIST_RECORD_TEMPLATE
    else:
        recordTemplate = ""

    return recordTemplate

def CreateItsoList(listType, format, numberRecords, listID, destinationISAM, outputFilename):
    messageCode = DetermineMessageCode(listType, format)
    if len(messageCode):
        if CheckDestinationISAM(destinationISAM):

            #
            # Setup dictionary for string substitutions
            #
            PLACE_HOLDER_DICTIONARY[ DESTINTATION_PLACE_HOLDER ] = destinationISAM
            PLACE_HOLDER_DICTIONARY[ MESSAGE_CODE_PLACE_HOLDER ] = messageCode

            recordTemplate = GetRecordTemplate(listType)

            #
            # create correct flavour of output
            #
            if format.lower() == "single":
                #CreateSingleList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename)
                CreateSingleList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename, no_commas=True)
            elif format.lower() == "multi":
                #CreateMultiList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename)
                CreateMultiList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename, no_commas=True)
            elif format.lower() == "nocommas":
                CreateNoCommasList(messageCode, numberRecords, recordTemplate, listID, destinationISAM, outputFilename)

    else:
        print( USAGE_STRING)

    print ("Created: %s" % outputFilename)

def CreateMultiRecordDataFrameFromIdList(f, listType, commas, recordNumber, idList):
    recordsInFrame = len(idList)
    messageCode = DetermineMessageCode(listType, "multi")
    PLACE_HOLDER_DICTIONARY[ MESSAGE_CODE_PLACE_HOLDER ] = messageCode
    recordTemplate = GetRecordTemplate(listType)

    CreateMultiRecordDataFrameHeader(f, recordTemplate, commas, recordsInFrame)

    for i in range (0, recordsInFrame):
        recordNumber = recordNumber + 1
        record = recordTemplate % (recordNumber, idList[i])
        if commas == False:
            record = record.replace(",", "")
        f.write("%s" % (record))

    CreateMultiRecordDataFrameTrailer(f)

def ResealXML(ftp2Folder, inputFilename, outputFilename):
    #
    # Reseal the inputfile to the output file using an I2F ISAM.
    #
    command = ITSOXMLResealerFullPath(ftp2Folder) + " -p I2F " + inputFilename + " " + outputFilename
    OsSystem(command)

def MakeItsoTable(ftp2Folder, sealedXMLFilename, workingFolder, messageFilename):
    command = MakeITSOTableFullPath(ftp2Folder) + " -ftp2day2 " + sealedXMLFilename + " " + os.path.join(workingFolder, messageFilename)
    OsSystem(command)

def CreateAndSealFile(ftp2Folder, listType, format, numberRecords, listID, destinationISAM, unsealedFilename, sealedFilename):
    CreateItsoList(listType, format, numberRecords, listID, destinationISAM, unsealedFilename)
    # awd: ResealXML(ftp2Folder, unsealedFilename, sealedFilename)

def AddTrailingBackSlash(folderName):
    if folderName[len(folderName) -1] != '/':
        folderName = folderName+ '/'
    return folderName

def MakeXMLFilenames(workingFolder, listType, format, numberRecords, listID, destinationISAM):

    if len(workingFolder):
        unsealedFilename = AddTrailingBackSlash(workingFolder)

    unsealedFilename = unsealedFilename + ("%s_%s_%d_%04x_%s" % (listType, format, numberRecords, listID, destinationISAM))
    sealedFilename = unsealedFilename + "_sealed"

    return (unsealedFilename + ".xml", sealedFilename + ".xml")

def MessageTypeNumberFromListType(listType):
    if listType.lower() == "hot":
        tableNumber = 3902
    elif listType.lower() == "action":
        tableNumber = 3901
    else:
        tableNumber = 666

    return tableNumber

def MakeMessageFilename(listType, listId):
    messageFilename = "MESSAGEFILE_00001_%05x_%010d.msg"%(MessageTypeNumberFromListType(listType), listId)
    return messageFilename

def CopyMessageFileToDestination(workingFolder, messageFilename, destinationFolder):
    shutil.copy(os.path.join(workingFolder, messageFilename), os.path.join(destinationFolder, messageFilename))

def BuildMessageFile(ftp2Folder, workingFolder, listType, format, numberRecords, listID, destinationISAM, destinationFolder):
    (unsealedXMLFilename, sealedXMLFilename) = MakeXMLFilenames(workingFolder, listType, format, numberRecords, listID, destinationISAM)
    CreateAndSealFile(ftp2Folder, listType, format, numberRecords, listID, destinationISAM, unsealedXMLFilename, sealedXMLFilename)
#    messageFilename = MakeMessageFilename(listType, listID)
#    MakeItsoTable(ftp2Folder, sealedXMLFilename, workingFolder, messageFilename)
#    CopyMessageFileToDestination(workingFolder, messageFilename, destinationFolder)
    # deleteTempFiles = True
    deleteTempFiles = False
    if deleteTempFiles:
        os.remove(unsealedXMLFilename)
        os.remove(sealedXMLFilename)
        os.remove(os.path.join(workingFolder, messageFilename))


def FormatFromXMLFilename(xmlFilename):
    format = ""
    if xmlFilename.lower().find("single") != -1:
        format = "single"
    if xmlFilename.lower().find("multi") != -1:
        format = "multi"
    if xmlFilename.lower().find("nocommas") != -1:
        format = "nocommas"
    return format


def VerifyParametersABit(ftp2Folder, listType, destinationISAM, listId, listsSizeKB, destinationFolder):
    result = True
    if not os.path.exists(ftp2Folder):
        print( "Failed to find FTP Folder: ", ftp2Folder)
        result = False
    if not (listType.lower() in ["hot", "action"]):
        print( "ListType (%s) not hot or action"%(listType))
        result = False
    elif len(destinationISAM) != 8:
        print( "Failed, ISAMID (%s) not length 8"%(destinationISAM))
        result = False
    elif not os.path.exists(destinationFolder):
        print( "Failed to find destination: ", destinationFolder)
        result = False
    return result

def CheckToolsPresent(ftp2Folder):
    result = True
    if not os.path.exists(MakeITSOTableFullPath(ftp2Folder)):
        print( "Failed to find tool: %s"%(MakeITSOTableFullPath(ftp2Folder)))
        result = False
    elif not os.path.exists(ITSOXMLResealerFullPath(ftp2Folder)):
        print( "Failed to find tool: %s"%(ITSOXMLResealerFullPath(ftp2Folder)))
        result = False
    return result


def DoCreateFTP2HotActionListMessageFiles(ftp2Folder, listType, destinationISAM, listId, listsSizeKB, destinationFolder):
    workingFolder = "WorkingFolder"
    CreateFolder(workingFolder )

    #
    # Hot or Action messages.
    #
    if listType.lower() == "hot":
        HotListRecordSize = CalculateRecordSize(HOT_LIST_RECORD_TEMPLATE)
        HotListRecords = int((listsSizeKB*1000) / HotListRecordSize)
        BuildMessageFile(ftp2Folder, workingFolder, "Hot",    "nocommas", HotListRecords,     listId, destinationISAM, destinationFolder)
        #BuildMessageFile(ftp2Folder, workingFolder, "Hot",    "multi", HotListRecords,     listId, destinationISAM, destinationFolder)
        #BuildMessageFile(ftp2Folder, workingFolder, "Hot",    "single", HotListRecords,     listId, destinationISAM, destinationFolder)
    elif listType.lower() == "action":
        ActionListRecordSize = CalculateRecordSize(ACTION_LIST_RECORD_TEMPLATE)
        ActionListRecords = int((listsSizeKB*1000) / ActionListRecordSize)
        #BuildMessageFile(ftp2Folder, workingFolder, "Action", "nocommas", ActionListRecords, listId, destinationISAM, destinationFolder)
        BuildMessageFile(ftp2Folder, workingFolder, "Action",    "multi", ActionListRecords, listId, destinationISAM, destinationFolder)
        #BuildMessageFile(ftp2Folder, workingFolder, "Action",    "single", ActionListRecords, listId, destinationISAM, destinationFolder)



def CreateFTP2HotActionListMessageFiles(ftp2Folder, listType, destinationISAMID, listId, listsSizeKB, destinationFolder):

    result = VerifyParametersABit(ftp2Folder, listType, destinationISAMID, listId, listsSizeKB, destinationFolder)
    if result:
        # Awd: this can go: result = CheckToolsPresent(ftp2Folder)
        if result:
             DoCreateFTP2HotActionListMessageFiles(ftp2Folder, listType, destinationISAMID, int(listId), int(listsSizeKB), destinationFolder)


#
# Main prog...
#
if len(sys.argv)== 7:
    CreateFTP2HotActionListMessageFiles(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
else:
    print( USAGE_STRING)

