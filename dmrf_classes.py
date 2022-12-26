class DomIdLoader:
    def __init__(self):
        self.offset_ = 1
        self.limit_ = 10
        self.url = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object'
        self.objects_data = None

    def get_ids(self):
        import requests
        paramz = {
            'offset': self.offset_,
            'limit': self.limit_,
            'sortField':'devId.devShortCleanNm',
            'sortType':'asc',
            'objStatus':'0',
        }
        res = requests.get(self.url, params=paramz)

        self.objects_data = res.json()

    def show_ids(self):
        # print()
        if not self.objects_data:
            print("No data loaded yet...")
            return
        objects_list = self.objects_data.get('data').get('list')
        ids = [x.get('objId') for x in objects_list]
        for one_id in ids:
            print(one_id)
    def return_ids(self):
        if not self.objects_data:
            print("No data loaded yet...")
            return
        objects_list = self.objects_data.get('data').get('list')
        return [x.get('objId') for x in objects_list]


class ObjectInfoExtractor:
    def __init__(self, ids):
        if not isinstance(ids, list):
            print("No list of ids is set!")
        elif not isinstance(ids[0], int):
            print("ids is not a list of integers!")
            return None
        self.idlist = ids
        self.dframe = None
        self.baseurl = "https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/"
        self.KeysDict = {'id': [], 'hobjId': [], 'pdId': [], 'developer': [], 'region': [],
                       'address': [], 'floorMin': [], 'floorMax': [], 'objElemLivingCnt': [], 
                       'objReady100PercDt': [], 'wallMaterialShortDesc': [], 'objLkFinishTypeDesc': [],
                       'objLkFreePlanDesc': [], 'objElemParkingCnt': [], 'objSquareLiving': [],
                       'rpdNum': [], 'rpdPdfLink': [], 'rpdIssueDttm': [], 'objLkLatitude': [],
                       'objLkLongitude': [], 'objCompensFundFlg': [], 'objProblemFlg': [],
                       'objLkClassDesc': [], 'loadDttm': [], 'photoRenderDTO': [],
                       'objGuarantyEscrowFlg': [], 'objectType': [], 'miniUrl': [],
                       'residentialBuildings': [], 'newBuildingId': [], 'objFloorCnt': [],
                       'objFlatCnt': [], 'objFlatSq': [], 'objNonlivElemCnt': [],  'objStatus': [],
                       'isAvailableWantLiveHere': [], 'objTransferPlanDt': [], 'objLivCeilingHeight': [],
                       'objInfrstrBicycleLaneFlg': [], 'objInfrstrPlaygrndCnt': [], 'objInfrstrSportGroundCnt': [],
                       'objInfrstrTrashAreaCnt': [], 'objInfrstrObjPrkngCnt': [], 'objInfrstrNotObjPrkngCnt': [],
                       'objInfrstrRampFlg': [], 'objInfrstrCurbLoweringFlg': [], 'objElevatorWheelchairCnt': [],
                       'objElevatorPassengerCnt': [], 'objElevatorCargoCnt': [], 'objElevatorCargoPassengerCnt': [],
                       'soldOutPerc': [], 'objPriceAvg': [], 'generalContractorNm': [], 'nonlivFirstFloor': [],
                       'objectTransportInfo': [], 'conclusion': [], 'objLkSaleDepEmail': [], 'objGreenHouseFlg': [],
                       'objEnergyEffShortDesc': [], 'infrastructureIndexValue': []}

    def load_data(self):
        import requests
        for idvalue in self.idlist:
            url = "{}{}".format(self.baseurl, idvalue)
            res = requests.get(url)
            object_data = res.json()
            for key in self.KeysDict:
                try:
                    self.KeysDict[key].append(object_data['data'][key])
                except:
                    self.KeysDict[key].append('-') 


    def df_converter(self):
        import pandas as pd
        if not self.KeysDict['id']:
            print("Load the date before converting!")
            return None
        self.dframe = pd.DataFrame.from_dict(self.KeysDict)
        

class Saver:
    def __init__(self, data):
        #will accept data as Pandas DataFrame
        import pandas as pd
        if not isinstance(data, pd.pandas.core.frame.DataFrame):
            print('Set data as Pandas DataFrame!')
            return None
        self.dframe = data
        
    def save_csv(self):
        # save pandas DF as CSV file
        # Comma Separated Values file
        self.dframe.to_csv('save_df.csv', index=False)
    
    def save_pickle(self):
        import pickle
        self.dframe.to_pickle('save_df.pickle')

    def save_xl(self):
        self.dframe.to_excel("save_df.xlsx")

    def save_sql(self):
        import pandas as pd
        import psycopg2
        connect_str = "dbname='DataScience' user='postgres' host='localhost' password='12345'" 
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        stmt = '''
        CREATE TABLE IF NOT EXISTS homes(
        id integer,
        region integer,
        address varchar(128),
        objReady100PercDt date
        )
        '''
        cursor.execute(stmt)
        ###
        stmt = '''
        INSERT INTO homes
        VALUES
        (%s, %s, %s, %s);
        '''
        
        # iterate DF to get the column we want
        for i in range(len(self.dframe)):
            cursor = conn.cursor()
            cursor.execute(stmt, (int(self.dframe['id'].iloc[i]), self.dframe['region'].iloc[i],
                                  self.dframe['address'].iloc[i], self.dframe['objReady100PercDt'].iloc[i]))
            conn.commit()
            cursor.close()
            
            

