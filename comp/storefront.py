import pandas as pd

def get_storefront_data():
    data_file = "data/Competitor Online Storefront Pr.csv"
    df = pd.read_csv(data_file)

    def check_online_storefront(row):
        if row['DTC Website'] == 'Yes' and row['E-commerce Functionality'] == 'Yes':
            return 'Yes'
        else:
            return 'No'

    df['Online Storefront Presence'] = df.apply(check_online_storefront, axis=1)
    final_table = df[['Brand', 'DTC Website', 'E-commerce Functionality', 'Online Storefront Presence']]
    final_table.columns = ['Brand Name', 'Has DTC Website', 'Has E-commerce Functionality', 'Has Online Storefront']
    final_table = final_table.sort_values(by='Brand Name')
    return final_table.to_dict(orient="records")