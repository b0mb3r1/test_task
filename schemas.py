from pydantic import BaseModel, PositiveInt


class ItemBase(BaseModel):
    item_group_id: PositiveInt
    mpn: PositiveInt
    title: str
    image_link: str
    additional_image_link: str
    link: str
    gender: str
    brand: str



class Product(ItemBase):
    id: str  # id + size
    price: str
    product_type: str
    size: str | None
    google_product_category: int

    def __init__(self, **kwargs):
        kwargs['price'] = f"{kwargs['price_amount']} {kwargs['currency_code']}"

        super().__init__(**kwargs)


class Item(ItemBase):
    class Size(BaseModel):
        size: str

        def __str__(self):
            return self.size
    availableSizes: list[Size]
    price_amount: PositiveInt
    currency_code: str

    def __init__(self, **kwargs):
        assert kwargs['type'] == 'Product'
        kwargs['item_group_id'] = kwargs['id']
        kwargs['mpn'] = kwargs['merchantId']
        kwargs['title'] = kwargs['shortDescription']
        kwargs['image_link'] = kwargs['images']['cutOut']
        kwargs['additional_image_link'] = kwargs['images']['model']
        assert kwargs['url']
        kwargs['link'] = 'https://www.farfetch.com' + kwargs['url']
        kwargs['brand'] = kwargs['brand']['name']
        kwargs['price_amount'] = kwargs['priceInfo']['finalPrice']
        kwargs['currency_code'] = kwargs['priceInfo']['currencyCode']

        super().__init__(**kwargs)


class Listing(BaseModel):
    class ListingItems(BaseModel):
        class Ad(BaseModel):
            adType: int
        items: list[Ad | Item]

    class ListingPagination(BaseModel):
        view: PositiveInt
        totalItems: PositiveInt
        totalPages: PositiveInt

    listingItems: ListingItems
    listingPagination: ListingPagination
