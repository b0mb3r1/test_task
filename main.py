import json
import re
import time
import requests
import xml.dom.minidom
import xml.etree.ElementTree as ET
from schemas import Listing, Item, Product
from playwright.sync_api import sync_playwright, Response

headers = {
    'Cookie': 'BIcookieID=ff774ad8-9635-4771-b3c7-c40213011ed6; ckm-ctx-sf=%2Fca; BISessionId=edda27b2-8fcd-60d0-3933-311e30bea559; __Host-FF.AppCookie=CfDJ8BZV7bSK_gVKoJ5_tFR15T4gcTa5RItAZX-iHTGF-caAn4WTYQTEz6AlYmd7CQho9AzTSV-2wt7iQuQmZ8A7XRHajNLgtMCbk3CT4Qz40B_VjKCcDYi8sPMXKaXx4DirCXL9XstJFSgQ79Fr0s18e1u78cScS83hB7cOwxyQQGvYJFj3EEza9eRmtcqRAWweCexDXbL8Gjt5QxVVwbsvc6UE0t9njrucsUODwuUI8G6oAeqWuDdsXTOr9bLql6wDva-eySOBF1Ue41JTDZPKfG52hLTs7aCUizxqo7jmJtBC; ffcp=a.1.0_f.1.0_p.1.0_c.1.0; ub=50CAC614848E6A27CBC86CA9829B46A4; ff_navroot_history=141258; ABProduct=; ABListing=; ABGeneral=; ABLanding=; ABCheckout=; ABRecommendations=; ABReturns=; ABWishlist=; __Host-CSRF-TOKEN=CfDJ8BZV7bSK_gVKoJ5_tFR15T5jUQ6tStq-R-vtf3hZu7GMqp-XW5itmQDYGCA1_ns8p-fXQaTtuIckVzi-euTiRz0LH-jodJkvRFy3fmrkeB8MXbiChAGjx2NbSqo7Sl6Ny2QDNbCIJpmHAu9FtQ48bwk; __Host-CSRF-REQUEST-TOKEN=CfDJ8BZV7bSK_gVKoJ5_tFR15T7qmJw_86Yxr484QQ0mVice-A2u5eMzVfkQDnqwNctPlG2oMCdx4-Q9L8zi31Q1nYJexa0XU7J22OgttSsif-lx0vMbXx30vnXyCNnlYqNe4G8nmTG6fl0EB4GPL7pOUcl1MNbYj-yuK4BXvNeBNZIZjeRi66gUY6JSaq9675biew; __Host-FF.AppSession=CfDJ8BZV7bSK%2FgVKoJ5%2FtFR15T50%2BFIKb%2FLtYpaJRTUHQnSLahn2kygAscjrpFvDX4c5It23DTF228FQMT8pAeAAZl5RMS4HA3GvMmoYu%2Fku%2Fr%2FiZ5iV3YJwUgsWGmbPD7QsBn2YpPfN3B6dPBSH2rTcqJI9jwn2nswzxF0ghieKykzY; AkamaiFeatureToggle=02a57c.1_0357f7.1_04154b.1_0a3efc.1_0f6c2f.431765611_1b443f.1171797472_1d8e03.1_1fc0ee.-1_20b92f.1_247006.-1_26ddb8.1_2ba087.1_317bfa.-555864285_3aa8d2.0_3c8089.2_4247d8.-210644093_45dc7d.1_48259b.1_4d76c8.2_4f9348.351382932_56f7db.-1_590a92.1_5a000f.1_5a745a.-1_5dbd1a.-1_5edc51.-1959550240_603919.1_613a9b.-416292886_64d19c.1_677d5c.351382932_6df3b9.-1_729a35.1_751ef1.-1_7723fd.-1_7cf0c5.-1_81160a.351382932_8c3210.-1_8c4007.-1_945679.1_999fce.2_9a710c.1_9d8620.-257072075_9ebcf7.1_9f0eda.1_9fca73.-1_a00510.1148090917_a27c87.1952121051_a54601.1_a7e49d.570408543_aa6446.-1671435226_ac992b.1_b45ee1.1_b833c7.535845473_b8e9db.-1_b90715.3_bf09c6.1_bf110c.-969915897_c06844.-1_c0ba66.-900375819_c2155c.1_c5e8eb.351382932_c6215a.-1_c7adc2.-1_ca11bd.274285006_ca47d2.-2125519295_cfc1ba.1_d052f2.909416419_d26d24.1_d2d2fd.-1_d47781.-1_d59758.1_da4cdf.1_dab09d.632075632_db79f1.2_dd19ed.-1_deb641.-1_dec9f3.-1_df039e.-1_df93a0.1_e7eec4.1_e89c2a.2_ed07fa.0_ed8d9e.1_ef0e65.-1_f02dd6.-1_f220ef.4_f3db94.1_f5969a.-1_f8c66b.1_fb273c.466665085_fb2b96.1_fb99aa.1171797472_fbf4d6.1_fdd39e.800640742; _abck=1BA37385B9190EE604B81040F6D656A5~0~YAAQNYAQAieF0CuPAQAAx3bhKwv6AvSxh7fD+rb3wSgVJ/MlurvDu64xuYBKFmPQc+vYzVoII6I+DcRbbvguE4gouFM3e63mRwxq6grrX8fPR7JhcXK6D1GlepZ8iT+Nc8pzbFxOS5yJuZjWk7f8MdwbrB376oNXpQMpO+z7NrQx5+hnzoT3cdmOjmrbYPyiv8U8No+mg1w1I4CSBRoRw7Ee7BA3iKpUnyM1ZUDdXbmvS2vbmgRC3hks8vehDEvYgz08ev1iPNmbepF4jwab4jKLZg0Bl6Z5wJNd9mlO9FuF2JJlOkV6YWiTs4E82oJOxnw7Qv6qfZG2yGd3NGc/mB/J4yOx7n+PmTv7OiA/cK7SHuuAmknM21LUoR7Mflrx8hCwBYlv/xiyeZpXzogP82j2Rsn0JWW8ulXJfmKERh84/BWEXvK0~-1~-1~1714431747; ak_bmsc=17D870A30BB5C24EFADC509D0D4B89EE~000000000000000000000000000000~YAAQNYAQAlWF0CuPAQAA037hKxe0Q1DFyaCX5m3VqyFSsg9yh7QuEBVhKryCwArgv9Lb6z2imaA6GV7bLrVeBRB5C97Zfzg+OBwRShFfjQWKZIGR8KH3UEwmOMcjlUxxFOefJqK5K0HB08FBBNNXeOYnsEvJa3uU5GK3OGvzy8xkbBdPcPubnAWYxehFe42FFjpVV5tcrhVnehrYnPrUa1BkYt20Be0SRG0VEOQWzHoOqSLj29C5krACxzZxuTjn4lCTOHAEf8+VKHYHh1SMg+TpWuar/91hC9r2nDAQDByMMyp+eGMNrCGpstuNa/RkQ2fK5Y3jP4G5ozIkp0rdejaQdgris5PeFR/cYGX1r8omT/zK5oUnFMGYzqRSxJ+AblqQt8vKm6GcQnfYQng+1wtW7vz+7H3AGBgMHDer6mBkMQdvROTumElujmGfydPuB7dyThdsyaEXxkvs; bm_sz=AB3F9BB0404C59E6BE83FE6B28CC8151~YAAQLz4SAvqGQCuPAQAAfnr/KxeO+v7AmddvoWPTN4yIsZhmt27ccerXUaL+BozIUTm3x7GxiZu9wqDQ78hRWKIBINnz5peJlZk2jnGDfn5RNjlJoHYH5QRUnRLlvZ8zUmmtdV9LGigwVZL0+U0/Yg4eD1Mg1CzRcx4G6Vr0Hd2SYh1lTRygbKyhJp5tJK7n8sq0k8ysNHI7E8SDQrw0Mk2esCxeqZjHYdTkt2MfM5dmIIVfnIToynSydd+BlfUgzKgFMBiP9vLTT+nrT5Fd4Aur7ZAKDPPr4v3CNiExW1BJrq3NJWL4BFYf5A8dg6ga+G9Zb5I953deQ16wNM9CvdZTMx8jpFPBDsfu8ygVnF5dmDYB+2RvlZM3LAD5/n78uhRehn94l/e/NfCjHbUTfvDtMowxNl9strcpbclTw5B9FR16DQ3Y2eYzd9UcX7v7KsxdF3OKSCJvxCSpa65vWxY+sVTtDXb+u8wYEw==~3748152~3686709; checkoutType2=4; session-1=edda27b2-8fcd-60d0-3933-311e30bea559; bm_sv=940F5E06B3864D218CB0703179044782~YAAQLz4SAvCOQCuPAQAAZYMALBfKmOTmviZiQEqF+VAImJrB8r0GlzZDnH8yJp432pTQZfP2mDDncs7qDOSgAZIhc6FgCxqYCbJdyIsySQVz0O5CWn7oEhVEYa/Ux4IuAmcRrqVE/hfIBKhG6J5V1RM7zbynMbo+0uhfekHB/Igr+e8V3lAIky8DU04odv1zw2OPFFFr1iG8j8qIHPTyCl98gWO4ND+JnDDkE4vWcz7GOjAv++KoeYixCCTGXcHFb63y~1; ff_newsletter_pv=1; _ga_HLS8C90D41=GS1.1.1714428148.1.1.1714429805.0.0.2093520121; _ga=GA1.1.451905340.1714428149; FPID=FPID2.2.cMNAZIm6xc7B2PSnaERjiJAgWob3%2FaaQqgGBRT1uorc%3D.1714428149; FPLC=XdXtD9mnZ8obYLNLjS5aLoXNwKevQ941zwkGGbHNxnmHTJRiXL0iPJXJQmVStdveMnR2QJXFZ8vbZUBJxzmrayqUAaP7y%2BgD7x543aHLSMskINbbSYqwdifLC44LYQ%3D%3D; FPAU=1.2.1947600891.1714428150; forterToken=1421f3f011d4486b8b0331c707742608_1714429802171__UDF43-m4_11ck_; _gcl_au=1.1.256026545.1714428150; RT="z=1&dm=www.farfetch.com&si=3a90175c-8d7b-4dce-9235-1aefe460056e&ss=lvli90a9&sl=6&tt=60v&obo=5&rl=1&nu=gd34b99d&cl=1849k"; _ga_CEF7PMN9HX=GS1.1.1714428149.1.1.1714429805.38.0.0; lastRskxRun=1714429802595; rskxRunCookie=0; rCookie=jejlauhf27pcw21pqvdpeglvli97q3; _gid=GA1.2.1933148798.1714428151; ftr_blst_1h=1714428151426; _cs_c=0; _cs_id=05376829-c910-ac99-f37b-5fb9d4ea60d2.1714428151.1.1714429806.1714428151.1.1748592151785.1; _cs_s=8.0.0.1714431606678; g_state={"i_p":1714435352856,"i_l":1}; cto_bundle=c--jZl94dWJQTXBlRTVQbFc2cnE1UXBDMyUyRlhmWEwxRTB2ZU1CblBPUmFYU2M1cnhHWkpGZXJTejRxdjYxa1RDajB3U2VRUmFJNEphcDVwN1g3OERrbmoySWFTMmkwWnlQRmljSnkwUzNJOGZqTVdQd2V5N3NUJTJGNkRRdk5JNW01MHAlMkJwZDJDclZKS0RVemwyMmg5Tjk5JTJCeGNUdyUzRCUzRA; _attn_=eyJ1Ijoie1wiY29cIjoxNzE0NDI4MTU1Mzg1LFwidW9cIjoxNzE0NDI4MTU1Mzg1LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImQ4NWZhZDdlMmI2ZjRmYWM5ZDkyYzk0MTI3NWM2YzA0XCJ9In0=; __attentive_id=d85fad7e2b6f4fac9d92c941275c6c04; __attentive_cco=1714428155386; __attentive_pv=8; __attentive_dv=1; __eoi=ID=8ff162b40ea9fb95:T=1714429783:RT=1714430174:S=AA-AfjZtN0rO_171l2PJ2LNKW6jR; __cuid=4725662633bc4623a5a3a08481c3e9c7; _uetsid=2d2b9e90067411efad085d266207f401; _uetvid=2d2bdbb0067411ef8e93d19262ca86bb',
}  # Request's headers
main_url = """https://www.farfetch.com/ca/plpslice/listing-api/products-facets?page=page&view=60&sort=3&pagetype=Shopping&rootCategory=Women&pricetype=FullPrice&c-category=135979"""


class Parser:
    def __init__(self):
        self.variations_json = None
        self.variations_json_text = None
        self.total_pages = None
        self.browser = None
        self.context = None
        self.browser = sync_playwright().start().chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.items = {}
        self.products = {}

    def run(self):
        self.get_total_pages()
        self.get_all_listings()

        self.get_all_products()

        self.context.close()
        self.browser.close()

    def get_all_listings(self):
        for page in range(1, self.total_pages + 1)[1:2]:  # Todo: Remove slice for production version
            print(f'Parsing {page=}')
            response = requests.get(url=main_url.replace('page=page', f'page={page}'), headers=headers)
            assert response.status_code == 200
            listing = Listing(**response.json())
            for item in listing.listingItems.items:
                if type(item) is Item:
                    # print(f'{item=}')
                    assert item.item_group_id  # It's not ad
                    self.items[item.item_group_id] = item
            time.sleep(2)
        print(f'Found {len(self.items)} unique items')

    def get_all_products(self):
        for item_id, item in self.items.items():
            breadcrumbs, sizes = self.get_variations(url=item.link)
            for size, price in sizes.items():
                prod_id = f'{item.item_group_id}_{size}'
                product = Product(**item.dict(),
                                  id=prod_id,
                                  price=price,
                                  size=size,
                                  product_type=breadcrumbs,
                                  google_product_category=2271)
                self.products[product.id] = product.model_dump()
            self.variations_json_text = None
            self.variations_json = None
            print(f'Parsed {len(self.products)} product variations')
            self.create_xml()

    def create_xml(self):
        root = ET.Element("rss", version="2.0", xmlns="http://base.google.com/ns/1.0")
        channel = ET.SubElement(root, "channel")
        title = ET.SubElement(channel, "title")
        title.text = "Farfetch"
        link = ET.SubElement(channel, "link")
        link.text = "https://www.farfetch.com/"
        description = ET.SubElement(channel, "description")
        description.text = "Farfetch shop"

        for product in self.products.values():
            product['description'] = ' '
            product['availability'] = 'in_stock'
            item = ET.SubElement(channel, "item")
            for key, value in product.items():
                subelement = ET.SubElement(item, key)
                subelement.text = str(value) if isinstance(value, (int, float)) else value
        xml_str = ET.tostring(root, encoding='utf-8').decode('utf-8')
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml_as_string = dom.toprettyxml()
        with open("output_2.xml", "w", encoding="utf-8") as file:
            file.write(pretty_xml_as_string)

    def get_variations(self, url):
        page = self.context.new_page()
        while True:
            try:
                self.current_url = url
                self.context.on("response", self.handle_response)
                print(f'{url=}')
                page.goto(url)
                page.wait_for_load_state(state='load')
                prod_html = page.content()
                pattern = re.compile(r'{"@context":"https://schema.org","@type":"BreadcrumbList"(.*?)</script><nav aria', re.DOTALL)
                product_json = pattern.search(prod_html)[0].split('</script><nav aria')[0]
                product_dict = json.loads(product_json)
                item_list_element = product_dict['itemListElement']
                breadcrumbs = []
                for item in item_list_element:
                    name = item['item']['name']
                    breadcrumbs.append(name)
                breadcrumbs = ' > '.join(breadcrumbs)
                assert self.variations_json
                sizes = {}
                for k, v in self.variations_json['apolloInitialState'].items():
                    if k.startswith('Variation'):
                        quantity = v.get('quantity', 0)
                        if quantity:
                            price = v['price']['value']['raw']
                            variation_ref = v['variationProperties'][0]['values'][0]['__ref']
                            size = self.variations_json['apolloInitialState'][variation_ref]['secondaryDescription']
                            sizes[size] = price

                page.close()
                return breadcrumbs, sizes
            except TypeError:
                print('Probably 429 error')
            time.sleep(10)

    def handle_response(self, response: Response):
        if response.url == self.current_url:
            resp_rext = response.text()
            if "__HYDRATION_STATE__" in resp_rext:
                self.variations_json_text = re.search('(?<=<script>window.__HYDRATION_STATE__=")[\w\W]+?(?=";[\w\W]+</script>)', resp_rext).group()
                self.variations_json_text = self.variations_json_text.replace('\\"', '"').replace('\\\\\\"', '\\"').replace('\\"', '"')
                self.variations_json = json.loads(self.variations_json_text)
            else:
                print(response.text())
                raise Exception('__HYDRATION_STATE__ not found in HTML')

    def get_total_pages(self):
        response = requests.get(url=main_url.replace('page=page', 'page=1'), headers=headers)
        assert response.status_code == 200
        listing = Listing(**response.json())
        self.total_pages = listing.listingPagination.totalPages
        time.sleep(5)


if __name__ == '__main__':
    parser = Parser()
    parser.run()
