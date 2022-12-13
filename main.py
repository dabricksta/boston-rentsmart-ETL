def main():
    call_Boston_gov_API(data_url, extracted_data_fn, 'boston-rent-smart-data-ddbr')
    clean_data(df)
    

if __name__ == '__main__':
    main()

