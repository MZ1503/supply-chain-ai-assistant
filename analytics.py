import pandas as pd

class Inventory:
    def __init__(self,csv_path): #only loading data this function is used

        #LOAD CSV
        self.df=pd.read_csv(csv_path)
        self.metrics=self._calculate_metrics()


    def _calculate_metrics(self):
        expired=self.df[self.df['DAYS_TO_EXPIRY']<0]
        actual_revenue=(self.df['ACTUAL_QTY']*self.df['UNIT_PRICE_AED']).sum()

       