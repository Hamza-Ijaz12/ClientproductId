import requests
import schedule
import time
import json
from funtionhandle import listchecking,sending_data_print,google_sheet,update_Seller_items_dic,update_old_seller_id,seller_brands_name



# Variables handling
asins = []
# Seller ID list to be imported


def repeatfuntion():
    from funtionhandle import old_seller_id,Seller_items_dic
    # print("===================================================")
    # print("Old Seller ID ",old_seller_id)
    # print("Dictionary--",Seller_items_dic)
    # print("===================================================")
    # Importing Client list
    seller_id =google_sheet()
    # print("New Data read from google sheet",seller_id)
    # print("Old Seller ID ",old_seller_id)
    # print("===================================================")

    # Calling the duntion to removed extra data from client dictoonary
    add_client,removed_client =listchecking(old_seller_id,seller_id)
    # print("removed client IDs ",add_client,"-------------",removed_client)
    # print("data dictionary before removal of removed client ids ",Seller_items_dic)
    # print("===================================================")
    for id in removed_client:
        del Seller_items_dic[id]
    # Updating the Old seller ID list for next time
    update_old_seller_id( seller_id)
   
    for id in seller_id:

        # URLs
            # Keepa API endpoint for product search
        url = "https://api.keepa.com/seller"

        # Data
            # Parameters for the API request
        params = {
                'key': 'bs4qoapu3qm8kofmcbutv1dga6nci2ml5c0j1is9mlneqrdffdml10tl9la70i3g',  # Your actual Keepa API key
                'domain': '2',  
                'seller': id , # The seller ID you have
                'storefront':1,
            }

            # Make the request to Keepa API
        response = requests.get(url, params=params)
        client_dic=response.json()
        # print(client_dic)
        print("+++++++++++++++++++++++++++++++++++++++")
        print(client_dic)
        print("+++++++++++++++++++++++++++++++++++++++")
        # Main funtion to handle list
        # print("Client Dictionary ----------------------------------------------------",client_dic)
        if 'sellers' in client_dic:
            seller_dic =client_dic['sellers']
            if seller_dic:
                res1 = next(iter(seller_dic))
                storebrand =seller_dic[res1] ['sellerBrandStatistics']
                # getting Only ASNI codes
                new_data =seller_dic[res1]['asinList']
                storename = seller_dic[res1]['sellerName']
        else:
            new_data=[]
        


        
        # Add olny if client ID is used for first time
        if id not in Seller_items_dic:
            old_data =[]
            Seller_items_dic[id]= new_data
        else:
            old_data = Seller_items_dic[id]
        






        # Calling the funtion for list evaluting
        add,removed = listchecking(old_data,new_data)
        brandnames = seller_brands_name(storebrand)
        # print("===================================================")
        # print("CLient Id ",id)
        # print("add and remove length",len(add),"------------",len(removed))
        # print("===================================================")
        if len(add)>0 or len(removed)>0:
            sending_data_print(add,removed,id,brandnames,storename)
        # Now store the new data in Dictonary 
        # print(Seller_items_dic[id])
        Seller_items_dic[id]= new_data
        # print("After changing",Seller_items_dic[id])
    update_Seller_items_dic(Seller_items_dic)
    
    


    

repeatfuntion()

schedule.every(4).hours.do(repeatfuntion)
# schedule.every(30).seconds.do(repeatfuntion)

while True:
    schedule.run_pending()
    