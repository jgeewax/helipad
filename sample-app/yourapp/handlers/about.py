import helipad

main, application = helipad.root('yourapp').static('/about/', {
    '':          'static/templates/about.html',
    'company/':  'static/templates/about_company.html'
})

if __name__ == '__main__':
    main()

