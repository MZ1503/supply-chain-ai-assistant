import pandas as pd

class Inventory:
    def __init__(self,csv_path): #only loading data this function is used
     
    
        #LOAD CSV
        self.df=pd.read_csv(csv_path)
        self.metrics=self._calculate_metrics()
        #Data validation
        print(self.df.isnull().sum())
        print(self.df.shape)
        print(self.df.dtypes)


    def _calculate_metrics(self):

             
         #1. How many products are expired?
        expired=self.df[self.df['DAYS_TO_EXPIRY']<0]


         #2. Which products are expiring in the next 7 days?
        exp_seven_days=self.df[(self.df['DAYS_TO_EXPIRY']>0 ) & (self.df['DAYS_TO_EXPIRY']<7)]
        
          #3.Which brand has the most expired products?
        top_expired_brand=self.df[self.df['DAYS_TO_EXPIRY']<0].groupby('BRAND').size().idxmax()
        
        #4. Which brand has the highest revenue?
        self.df['REVENUE']=self.df['ACTUAL_QTY']*self.df['UNIT_PRICE_AED']
        top_revenue_brand=self.df.groupby('BRAND')['REVENUE'].sum().idxmax()

        #5. What is the total inventory value?
        total_inv_val=(self.df['ACTUAL_QTY']*self.df['UNIT_PRICE_AED']).sum() 

        #6. Which category has the most stock?
        highest_stock_category=self.df.groupby('CATEGORY')['ACTUAL_QTY'].sum().idxmax()

        #7. Which products have zero stock?
        products_zero_stock=self.df[self.df['ACTUAL_QTY']==0]

        #8. What is the expiry rate by brand?
        total_prod_brand=self.df.groupby('BRAND').size()
        expired_prod_brand=self.df[self.df['DAYS_TO_EXPIRY']<0].groupby('BRAND').size()
        expiry_rate=(expired_prod_brand/total_prod_brand*100).fillna(0).round(2)

        #9. Which brands need urgent attention?
        urgent_brands=expiry_rate[expiry_rate>20].index.to_list()

        #10. Show me the top 10 products by stock value?
        top_10_products=self.df.sort_values('REVENUE',ascending=False).head(10)
        return {
        "expired_count": len(expired),
        "expiring_7_days": exp_seven_days.to_dict('records'), #why dict? why not list?
        "top_expired_brand":top_expired_brand,
        "top_revenue_brand":top_revenue_brand,
        "total_inv_val":total_inv_val,
        "highest_stock_category":highest_stock_category,
        "products_zero_stock":products_zero_stock.to_dict('records'), #why dict? why not list?
        "expiry_rate_brand":expiry_rate.to_dict(), #why dict? why not list?
        "urgent_brands": expiry_rate[expiry_rate > 20].index.tolist(),
        "top_10_products": top_10_products[['BRAND', 'CATEGORY', 'ACTUAL_QTY', 'REVENUE']].to_dict('records')
               }

if __name__ == "__main__":
    inventory = Inventory("data/my_actual_alseer_portfolio.csv")
    print(inventory.metrics)