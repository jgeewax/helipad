Helipad is a really simple "micro-framework" that makes it easy to do the stupid
stuff really quickly on Google AppEngine.

### ... Another one of these pieces of crap? You've got to be kidding.

As great as AppEngine is, it seemed like some stupid stuff (like the Hello World)
built with `webapp` was more verbose than it needed to be. I figured that there
must be a way to be a bit more terse without losing any clarity. This little file
has a few helpers that are just shorthand for things that you can do with `webapp`.

Getting started with helipad is simple. Put `helipad.py` file in the directory where
your application is and `import helipad`.

### Take a look at the sample application

[sample-app/yourapp/handlers/](http://github.com/jgeewax/helipad/tree/master/sample-app/yourapp/handlers/)

### Basic request handlers

`app.yaml`

    handlers:
    - url: /helloworld/
      script: yourapp/handlers/helloworld.py
    
    - url: /pages/.*
      script: yourapp/handlers/pages.py
    
    - url: /pages-prefixed/.*
      script: yourapp/handlers/pages_prefixed.py
    
    - url: /pages-unordered/.*
      script: yourapp/handlers/pages_unordered.py

`yourapp/handlers/helloworld.py`

    import helipad

    class HelloWorldHandler(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad World!')

    main, application = helipad.app(HelloWorldHandler)

    if __name__ == "__main__":
      main()


`yourapp/handlers/pages.py`

    import helipad

    class Page1(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page1')

    class Page2(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page2')

    main, application = helipad.app([
      ('/pages/page1/', Page1),
      ('/pages/page2/', Page2),
    ])

    if __name__ == "__main__":
      main()

`yourapp/handlers/pages_prefixed.py`

    import helipad

    class Page1(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page1')

    class Page2(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page2')

    main, application = helipad.app('/pages-prefixed/', [
      ('page1/', Page1),
      ('page2/', Page2),
    ])

    if __name__ == "__main__":
      main()

`yourapp/handlers/pages_unordered.py`

    import helipad

    class Page1(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page1')

    class Page2(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page2')

    main, application = helipad.app('/pages-unordered/', {
      'page1/': Page1,
      'page2/': Page2,
    })

    if __name__ == "__main__":
      main()

### Serving static files

Template should be put in `yourapp/tempates/about.html`

`app.yaml`

    application: yourapp
    version: 1
    runtime: python
    api_version: 1
    
    handlers:
    - url: /about/
      script: yourapp/handlers/about.py
    
    - url: /about-shortcut/
      script: yourapp/handlers/about_shortcut.py
    
    - url: /about-multiple/.*
      script: yourapp/handlers/about_multiple.py

`yourapp/handlers/about.py`

    import helipad

    class StaticPage(helipad.Handler):
      def get(self):
        self.static('templates/about.html')
    
    # This tells helipad what module the path is relative to:
    helipad.root('yourapp')
    
    main, application = helipad.app(StaticPage)

    if __name__ == "__main__":
      main()

`yourapp/handlers/about_shortcut.py`

    import helipad

    main, application = helipad.root('yourapp').static('templates/about.html')

    if __name__ == "__main__":
      main()


`yourapp/handlers/about_multiple.py`

    import helipad

    main, application = helipad.root('yourapp').static('/about-multiple/', {
      '':          'templates/about.html',
      'company/':  'templates/about_company.html',
    })

    if __name__ == "__main__":
      main()
    
    

