import requests
from lxml import etree
import json
from flask import Flask,request

amz_url = 'https://www.amazon.in/dp/B0BQHS8L8Z?ref_=cm_sw_r_cp_ud_dp_82VAQDN1E3CD7DEYKPZ6'
flp_url = ' http://dl.flipkart.com/dl/canon-pixma-mg3070s-multi-function-wifi-color-inkjet-printer/p/itmehvnb3zxjwy9f?pid=PRNEHVNB6R7HTWGG&cmpid=product.share.pp&lid=LSTPRNEHVNB6R7HTWGGJ3E0MV'
mnt_url = 'https://www.myntra.com/casual-shoes/nike/-nike-sb-chron-2-textured-sneakers/23441354/buy'
ajo_url = 'https://www.ajio.com/crocs-unisex-literide-clog/p/469430410_grey'

def flp_price(flp):
    response = requests.get(flp, headers={"User-Agent": "Mozilla/5.0 ( Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})

    if response.status_code == 200:
        html = etree.HTML(response.content)
        script_tags = html.xpath('//script[@type="application/ld+json"]')
        script_content = script_tags[0].text
        script_data = json.loads(script_content)
        return str(script_data[0].get("offers", {}).get("price"))
    else:
        return 'Error'

def mnt_price(mnt):
    response = requests.get(mnt, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        html = etree.HTML(response.content)
        script_tags = html.xpath('//script[@type="application/ld+json"]')
        script_content = script_tags[1].text
        script_data = json.loads(script_content)
        return script_data.get("offers", {}).get("price")
    else:
        return 'Error'

def ajo_price(ajo):
    response = requests.get(ajo, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        html = etree.HTML(response.content)
        script_tags = html.xpath('//script[@type="application/ld+json"]')
        script_content = script_tags[2].text
        script_data = json.loads(script_content)
        return script_data.get("offers", {}).get("price")
    else:
        return 'Error'


app = Flask(__name__)


@app.route('/',methods=['GET'])
def home():
    return 'Welcome to Price Tracker API'


@app.route('/ajio/',methods=['GET'])
def ajo():
    try:
        query = str(request.args.get('url'))
        if query == '':
            return 'No URL'
        else:
            return ajo_price(query)
    except:
        return 'Error'


@app.route('/myntra/',methods=['GET'])
def mnt():
    try:
        query = str(request.args.get('url'))
        if query == '':
            return 'No URL'
        else:
            return mnt_price(query)
    except:
        return 'Error'


@app.route('/fkart/',methods=['GET'])
def flp():
    try:
        query = str(request.args.get('url'))
        if query == '':
            return 'No URL'
        else:
            return flp_price(query)
    except:
        return 'Error'


if __name__ == "__main__":
    app.run()
