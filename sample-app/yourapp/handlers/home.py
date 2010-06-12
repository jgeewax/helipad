import helipad

main, application = helipad.root('yourapp').static('static/templates/home.html')

if __name__ == '__main__':
    main()

