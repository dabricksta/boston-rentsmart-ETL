import extract_data
import clean_data

def main():
    extract_data.call_boston_gov_api('boston-rent-smart-data-ddbr')
    clean_data.clean_data()
    

if __name__ == '__main__':
    main()