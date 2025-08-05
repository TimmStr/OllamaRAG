import pandas as pd

from utils.constants import DEFAULT_DATASET_PATH, PRODUCT, DATE, PRICE


# most_sold_item = df.groupby([PRODUCT, NAME, MONTH], as_index=False).agg(
#     price=(DATE, 'count'),
#     size=(QUANTITY, 'sum'),


def read_csv():
    df = pd.read_csv(DEFAULT_DATASET_PATH)
    most_sold_item = df.groupby([PRODUCT], as_index=True).agg(
        sold_products=(DATE, 'count'),
        cumulated_price=(PRICE, 'sum')
    )
    print(most_sold_item.columns)
    most_sold_item = most_sold_item.sort_values(by="sold_products")
    print(most_sold_item)


read_csv()
