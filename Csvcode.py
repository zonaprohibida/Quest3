"""
CSE7390 Quest 3: Working with CSV Files

The following python module will read the csv file and create a dictionary where the keys are the regions and the values are 
a list of dictionaries, one for each well. Each row in the csv refers to a unique well.
"""

__STUDENT_ID__  = "47555408"
__CODING_NAME__ = "tkyaagba"

#import declarations
import csv
import pprint

__CSV_FILE__ = 'Wells.06.03.18Rigs.CSV'
__REGION__ = 'OFS Region'
__RIGNAME__ = 'Rig Name/Number'
__STATE__ = 'State/Province'
__OPERATOR__ = 'Operator Name'
__CONTRACTOR__ = 'Contractor Name'
__RIG_LAT__ = 'Rig Latitude (WGS84)'
__RIG_LONG__ = 'Rig Longitude (WGS84)'



def genRegionDictFromCsv(csvfile):
    with open(csvfile, newline='') as infile:
        data = list(csv.reader(infile))
    
    #get indexes of all columns of interest
    region = data[0].index(__REGION__)
    rigname = data[0].index(__RIGNAME__)
    state = data[0].index(__STATE__)
    operator = data[0].index(__OPERATOR__)
    contractor = data[0].index(__CONTRACTOR__)
    rig_lat = data[0].index(__RIG_LAT__)
    rig_long = data[0].index(__RIG_LONG__)
    
    firstRow = data.pop(0)

    kList = ['rigname', 'region', 'state', 'operator', 'contractor', 'rig_lat', 'rig_long']
    vList = [rigname, region, state, operator, contractor, rig_lat, rig_long]
    
    regionDict = {}

    for row in data:
        tempDict = {}
        for value in vList:
            key = kList[vList.index(value)]
            tempDict[key] = row[value]
            
        if row[region] in regionDict.keys():
            regionDict[row[region]].append(tempDict)
        elif not row[region] == '':
            regionDict[row[region]] = [tempDict]
            
    pp = pprint.PrettyPrinter(indent=3)
    pp.pprint(regionDict)


def main():
    genRegionDictFromCsv(__CSV_FILE__)

if __name__ == '__main__': main()
    