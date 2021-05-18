import re
import json
#use this function to clean root namespace URI
def namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''

def normalize_offerItems(root, filename):
    # Get URI cleaned
    rootCleaned = namespace(root)

    # get offered items
    offerItems = root.findall('.//'+rootCleaned+'ALaCarteOfferItem')
    #creating dict to parse
    rowDict = dict()

    if(len(offerItems) > 0):
        offerItemsPrice = dict()
        for item in offerItems:
            offerItemsPrice[item.get('OfferItemID')] = dict()
            code = item.find('.//'+rootCleaned+'SimpleCurrencyPrice')
            offerItemsPrice[item.get('OfferItemID')]['price'] = code.text
            offerItemsPrice[item.get('OfferItemID')]['price'] = code.text
            offerItemsPrice[item.get('OfferItemID')]['currencyType'] = code.get('Code')

        cabinLayoutDic = dict()

    for seatMap in root.findall('.//'+rootCleaned+'SeatMap'):
        for row in seatMap.findall('.//'+rootCleaned+'Row'):
            rowNumber = row.find('.//'+rootCleaned+'Number').text

            cabinAux = seatMap.findall('.//'+rootCleaned+'CabinLayout')
            cabinLayout = ""

            for aux in cabinAux[0].findall('.//'+rootCleaned+'Columns'):
                if(aux.text is not None):
                    cabinLayout += aux.text
                    cabinLayoutDic[aux.get('Position')] = aux.text
                else:
                    cabinLayout += " "
                    cabinLayoutDic[aux.get('Position')] = 'NONE'

            rowDict[rowNumber] = dict()
            rowDict[rowNumber]['cabinType'] = cabinLayout

            for seat in row.findall('.//'+rootCleaned+'Seat'):
                seatPos = seat.find('.//'+rootCleaned+'Column').text
                SeatFeature = cabinLayoutDic[seatPos]

                if seat.find('.//'+rootCleaned+'OfferItemRefs') is not None:
                    offerItemsRef = seat.find(
                        './/'+rootCleaned+'OfferItemRefs').text
                    price = offerItemsPrice[offerItemsRef]['price']
                    currencyType = offerItemsPrice[offerItemsRef]['currencyType']
                else:
                    price = 'Not available'
                    currencyType = 'Not available'

                rowDict[rowNumber]['price'] = price
                rowDict[rowNumber]['currencyType'] = currencyType
                rowDict[rowNumber][seatPos] = dict()
                
                for seatID in seat:
                    if 'SeatDefinitionRef' in str(seatID.tag):
                        rowDict[rowNumber][seatPos][seatID.text] = dict()
                        rowDict[rowNumber][seatPos][seatID.text]['Features'] = SeatFeature
            
    with open(filename+'.json', 'w') as fp:
        json.dump(rowDict, fp, indent=4, sort_keys=True)


def normalize_envelope(root, filename):
    rootCleaned = namespace(root[0][0])
    rowDict = dict()

    for rowInfo in root.findall('.//'+rootCleaned+'RowInfo'):
        rowDict[rowInfo.get('RowNumber')] = dict()
        rowDict[rowInfo.get('RowNumber')]['cabinClass']= rowInfo.get('CabinType')
        seats = []
        
        rowDict[rowInfo.get('RowNumber')][rowInfo.get('CabinType')] = dict()
        for seat in rowInfo.findall('.//'+rootCleaned+'SeatInfo'):
            seats.append((seat.find('.//'+rootCleaned+'Summary').get('SeatNumber')))

            seatNumber = seat.find('.//'+rootCleaned+'Summary').get('SeatNumber')
            rowDict[rowInfo.get('RowNumber')][rowInfo.get('CabinType')][seatNumber] = dict()

            features = []
            for feature in seat.findall('.//'+rootCleaned+'Features'):
                if feature.text == "Other_":
                    features.append(feature.get('extension'))
                else:
                    features.append(feature.text)

            if seat.findall('.//'+rootCleaned+'Service'):
                rowDict[rowInfo.get('RowNumber')][rowInfo.get('CabinType')][seatNumber]['Price']= seat.find('.//'+rootCleaned+'Fee').get('Amount')
            
            rowDict[rowInfo.get('RowNumber')][rowInfo.get('CabinType')][seatNumber]['Feature']= features
            

        

        with open(filename+'.json', 'w') as fp:
            json.dump(rowDict, fp, indent=4, sort_keys=True)