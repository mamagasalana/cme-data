

def edit_chromedriver():
    bytes_in  = '$cdc_asdjflasutopfhvcZLmcfl_'.encode('ASCII')
    bytes_out = '$btlhsaxdbTXgBATaKvTRhvcZLm_'.encode('ASCII')

    bytes_in2 = 'cdc_adoQpoasnfa76pfcZLmcfl'.encode('ASCII')
    bytes_out2 = 'btlhsaxdbTXgBATaKvTRhvcZLm'.encode('ASCII')

    with open('chromedriver.exe', 'rb') as f:
        a = f.read()
    
    a = a.replace(bytes_in, bytes_out)
    a = a.replace(bytes_in2, bytes_out2)

    with open('chromedriver.exe', 'wb') as f:
        f.write(a)
        
if __name__ == '__main__':
    print(edit_chromedriver())