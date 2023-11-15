# Required Library
import pymongo
import pandas as pd

# Mongo Db Connectivity
Mongo = pymongo.MongoClient('mongodb+srv://praveen:praveenroot@praveen21.lsdge0t.mongodb.net/?retryWrites=true&w=majority')

# Database & Collection Created
db = Mongo['sample_airbnb']
collection = db['listingsAndReviews']

# Total Documents
Documents = [i for i in collection.find()]
len(Documents)

# Collecting Relevant Data
res = [i for i in collection.find({},{'_id':1,'name':1,'description':1,'host.host_id':1,'host.host_name':1,'host.host_neighbourhood':1,'address.location.coordinates':1,'price':1, 'availability.availability_30':1 , 'availability.availability_60':1 ,'availability.availability_90':1 ,'availability.availability_365':1,'room_type':1,'minimum_nights':1,'maximum_nights':1 ,'number_of_reviews':1,'host.host_total_listings_count':1,'review_scores.review_scores_rating':1,'review':1,'amenities':1,'property_type':1})]

# Initialize data dictionary
data = {'Id':[], 'Name':[], 'Description':[], 'Property Type':[], 'Room Type':[], 'Minimum Nights':[],
        'Maximum Nights':[], 'Number Of Reviews':[], 'Amenities':[], 'Price':[], 'Host ID':[], 'Host Name':[],
        'Host Neighbourhood':[], 'Host Total Listings Count':[], 'Longitude':[], 'Latitude':[], 'Availability 30':[],
        'Availability 60':[], 'Availability 90':[], 'Availability 365':[], 'Rating':[]}

# Fill data dictionary
for i in res:
    data['Id'].append(i['_id'])
    data['Name'].append(i['name'])
    data['Description'].append(i['description'])
    data['Property Type'].append(i['property_type'])
    data['Room Type'].append(i['room_type'])
    data['Minimum Nights'].append(i['minimum_nights'])
    data['Maximum Nights'].append(i['maximum_nights'])
    data['Number Of Reviews'].append(i['number_of_reviews'])
    data['Amenities'].append(i['amenities'])
    data['Price'].append(i['price'])
    data['Host ID'].append(i['host']['host_id'])
    data['Host Name'].append(i['host']['host_name'])
    data['Host Neighbourhood'].append(i['host']['host_neighbourhood'])
    data['Host Total Listings Count'].append(i['host']['host_total_listings_count'])
    data['Longitude'].append(i['address']['location']['coordinates'][0])
    data['Latitude'].append(i['address']['location']['coordinates'][1])
    data['Availability 30'].append(i['availability']['availability_30'])
    data['Availability 60'].append(i['availability']['availability_60'])
    data['Availability 90'].append(i['availability']['availability_90'])
    data['Availability 365'].append(i['availability']['availability_365'])
    data['Rating'].append(i['review_scores']['review_scores_rating'] if 'review_scores_rating' in i['review_scores'] else 0)

# Convert data into structured format
df = pd.DataFrame(data)

# Empty String Value Replace
df['Description'] = df['Description'].apply(lambda x: 'not mentioned' if x == '' else x)
df['Name'] = df['Name'].apply(lambda x: 'not mentioned' if x == '' else x)
df['Host Neighbourhood'] = df['Host Neighbourhood'].replace("", method='ffill')

# Save "Airbnb" Data Csv File
df.to_csv('Airbnb.csv', index=False)
