import json
import xml.etree.ElementTree as ET
import re
from functions import normalize_offerItems as NO
from functions import normalize_envelope as NE
import sys

filename = sys.argv[-1]
filename_fixed = filename.split('.')[0]

tree = ET.parse("seatmap1.xml")
root = tree.getroot()

if 'SeatAvailabilityRS'in root.tag:
    NO(root, filename_fixed)
else:
    NE(root, filename_fixed)

# rootCleaned = namespace(root[0][0])
# rowDict = dict()

# for rowInfo in root.findall('.//'+rootCleaned+'RowInfo'):
#     rowDict[rowInfo.get('RowNumber')] = dict()
#     rowDict[rowInfo.get('RowNumber')]['cabinClass']= rowInfo.get('CabinType')
#     seats = []
    
#     rowDict[rowInfo.get('RowNumber')][rowInfo.get('CabinType')] = dict()
#     for seat in rowInfo.findall('.//'+rootCleaned+'SeatInfo'):
#         seats.append((seat.find('.//'+rootCleaned+'Summary').get('SeatNumber')))

#         seatNumber = seat.find('.//'+rootCleaned+'Summary').get('SeatNumber')
#         rowDict[rowInfo.get('RowNumber')][rowInfo.get('CabinType')][seatNumber] = dict()

#         features = []
#         for feature in seat.findall('.//'+rootCleaned+'Features'):
#             if feature.text == "Other_":
#                 features.append(feature.get('extension'))
#             else:
#                 features.append(feature.text)

#         if seat.findall('.//'+rootCleaned+'Service'):
#             rowDict[rowInfo.get('RowNumber')][rowInfo.get('CabinType')][seatNumber]['Price']= seat.find('.//'+rootCleaned+'Fee').get('Amount')
#         else:
#             print(False)
        
#         rowDict[rowInfo.get('RowNumber')][rowInfo.get('CabinType')][seatNumber]['Feature']= features
        

    

# with open('seatmap1.json', 'w') as fp:
#     json.dump(rowDict, fp, indent=4, sort_keys=True)

    

#NO(root)