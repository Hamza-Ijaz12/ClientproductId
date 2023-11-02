import requests

import gspread
from itertools import chain
import json



Seller_items_dic={}
old_seller_id = []



# Webhook.site URL

# funtion to find values and send
def listchecking(old,new):
    new_added = []
    removed_item = []
    for i in new:
        if i not in old:
            new_added.append(i)
    
    for i in old:
        if i not in new:
            removed_item.append(i)
    
    return new_added,removed_item


def sending_data_print(new_added,removed_item,ID,storenames,storename):
    webhook_url='https://discord.com/api/webhooks/1167805905086185634/tN-1qmwkbB9IvDoG0ZK6dKOxy_Q1pVemFNqWqu9TJ5xeQB4ccVJBPAnKrDcSxgatzDMv'
    # Mine Discord link
    # webhook_url='https://discordapp.com/api/webhooks/1167172079586643990/P95xBuVwUg02N50Qnv7UgT_orYLWEVuADoc2OWXGWOMCDcnY_0xaN7S0fS47iwH1Fof4'
    
    name = ID
    message_content = f'Here is the update\n\n Brand names with product count {storenames}\n\nAdded qty: {len(new_added)} and Removed qty: {len(removed_item)} \n\n Add items: {new_added} \n\n Removed Items : {removed_item}'

    data = {
        "content": f'Client Name: {storename}({name})',
        "embeds": [
            {
                "title": f"Client Name: {storename}",
                "description": message_content,
                "color": 65280  # You can customize the embed color
            }
        ]
    }

    headers = {'Content-Type': 'application/json'}

    r  = requests.post(webhook_url, json=data, headers=headers)



    
    
    # data = {"Client_ID":ID,"Added":new_added,"Added-qty":len(new_added),"Removed":removed_item,"Removed-qty":len(removed_item)}
    # r = requests.post(web_url,json=data,headers={"content-type":"application/json"})
    # print("Newly added Item codes ", new_added)
    # print("number of added items",len(new_added))
    # print("removed Item codes ", removed_item)
    # print("number of removed items",len(removed_item))




def google_sheet():
    sa = gspread.service_account(filename='account_k.json')
    sh = sa.open('Testing')

    wks = sh.worksheet('Sheet1')
    a= wks.get_all_values()

    flattened_data = list(chain(*a))
    flattened_data = flattened_data[1:]
    return flattened_data

def update_old_seller_id(new_data):
    global old_seller_id
    old_seller_id = new_data
    # print("++++++++++++++++++++++++++++++++++++")
    # print("Seller Id from funtion----------------------------------------------",old_seller_id)
    # print("++++++++++++++++++++++++++++++++++++")

def update_Seller_items_dic(new_data):
    global Seller_items_dic
    Seller_items_dic = new_data
    # print("++++++++++++++++++++++++++++++++++++")
    # print("Seller dic from funtion----------------------------------------------",Seller_items_dic)
    # print("++++++++++++++++++++++++++++++++++++")


def seller_brands_name(brand_dic):
    brandslist= []
    for item in brand_dic:
        a=[item['brand'],item['productCount']]
        brandslist.append(a)
    return brandslist

