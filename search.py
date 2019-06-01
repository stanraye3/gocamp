import requests
import uuid

HEADERS_JSON = {'Content-Type': 'application/json'}

ENDPOINTS = {
    'LIST_RESOURCETYPES': 'https://washington.goingtocamp.com/api/resourcecategory',
    'LIST_RESOURCESTATUS': 'https://washington.goingtocamp.com/api/availability/resourcestatus',
    'MAPDATA': 'https://washington.goingtocamp.com/api/maps/mapdatabyid',
    'LIST_CAMPGROUNDS': 'https://washington.goingtocamp.com/api/resourcelocation/rootmaps',
    'SITE_DETAILS': 'https://washington.goingtocamp.com/api/resource/details',
    'CAMP_DETAILS': 'https://washington.goingtocamp.com/api/resourcelocation/locationdetails',
    'DAILY_AVAILABILITY': 'https://washington.goingtocamp.com/api/availability/resourcedailyavailability',
}


def main():
    camps_by_resourcelocationid = {}
    camps_by_mapid = {}
    for camp in list_camps():
        if camp['resourceLocationId'] and -2147483648 in camp[
            'resourceCategoryIds']:  # -2147483648 = campground (from LIST_RESOURCETYPES)
            camps_by_resourcelocationid[camp['resourceLocationId']] = camp['resourceLocationLocalizedValues']['en-US']
            camps_by_mapid[camp['mapId']] = camp['resourceLocationLocalizedValues']['en-US']

    # details = []
    # for id, name in camps_by_resourcelocationid.items():
    #     details.append(get_camp_detail(id))
    # print(details)

    for camp_id, camp_name in camps_by_mapid.items():
        print(camp_name)
        for camp_area_id, camp_area_info in list_camp_areas(camp_id).items():
            print(camp_area_info)
            sites = get_site_availability(camp_area_id)
            for site in sites:
                site_info = get_site_detail(camp_area_id)
                print(' SITE:%s'%site_info)
                print(' AVAIL:%s'%site)


def list_camps():
    return requests.get(ENDPOINTS['LIST_CAMPGROUNDS']).json()


def get_camp_detail(resourcelocationid):
    return requests.get(ENDPOINTS['CAMP_DETAILS'],params={'resourceLocationId':resourcelocationid}).json()


def get_site_detail(resourceId):
    return requests.get(ENDPOINTS['SITE_DETAILS'],params={'resourceId':resourceId}).json()


def get_site_availability(resourceId):
    params = {
        'resourceId': resourceId,
        'cartUid':uuid.uuid4(),
        'startDate':'2019-07-01T07:00:00.000Z',
        'endDate':'2020-10-01T06:59:59.999Z',
        'equipmentId':'32768'

    }
    return requests.get(ENDPOINTS['DAILY_AVAILABILITY'],params=params).json()


def list_camp_areas(mapid):
    data = {
       'mapId':mapid,
       'bookingVersion':{
          'bookingCapacityCategoryCounts':[
             {
                'capacityCategoryId':-32767,
                'subCapacityCategoryId':None,
                'count':1
             }
          ],
          'rateCategoryId':-32768,
          'startDate':'2019-06-01T14:00:00.000Z',
          'endDate':'2019-06-02T14:00:00.000Z',
          'releasePersonalInformation':False,
          'equipmentCategoryId':-32768,
          'subEquipmentCategoryId':-32768,
          'requiresCheckout':False,
          'bookingStatus':0,
          'completedDate':'2019-06-01T12:38:32.676Z'
       },
       'bookingCategoryId':0,
       'startDate':'2019-06-01T07:00:00.000Z',
       'endDate':'2019-06-02T07:00:00.000Z',
       'isReserving':False,
       'getDailyAvailability':True,
       'partySize':1,
       'equipmentId':-32768,
       'subEquipmentId':-32768,
       'generateBreadcrumbs':False
    }
    results = requests.post(ENDPOINTS['MAPDATA'], headers=HEADERS_JSON, json=data).json()
    camp_areas_by_id = {}
    for id, info in results['mapLinkLocalizedValues'].items():
        camp_areas_by_id[id] = [(entry['title'],entry['description']) for entry in info]
    return camp_areas_by_id


main()