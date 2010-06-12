## What the hell is helipad?

Helipad is a really simple "micro-framework" that makes it easy to do the stupid
stuff really quickly on Google AppEngine.

### ... Another one of these pieces of crap? You've got to be kidding.

As great as AppEngine is, it seemed like some stupid stuff (like the Hello World)
built with `webapp` was more verbose than it needed to be. I figured that there
must be a way to be a bit more terse without losing any clarity. This little file
has a few helpers that are just shorthand for things that you can do with `webapp`.

## Quickstart guide

Getting started with helipad is simple. Put `helipad.py` file in the directory where
your application is and `import helipad`.

## Showcase

### Hello helipad!

#### app.yaml

    application: your-app-id
    version: 1
    runtime: python
    api_version: 1

    handlers:
    - url: /helloworld/
      script: yourapp/handlers/helloworld.py

#### yourapp/handlers/helloworld.py:

    import helipad

    class HelloWorldHandler(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad World!')

    main, application = helipad.app(HelloWorldHandler)

    if __name__ == "__main__":
      main()

### Multiple handlers in one file:

#### app.yaml

    application: your-app-id
    version: 1
    runtime: python
    api_version: 1

    handlers:
    - url: /pages/.*
      script: yourapp/handlers/pages.py

#### yourapp/handlers/pages.py

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

### Multiple handlers in one file, with prefixes:

#### app.yaml

    application: your-app-id
    version: 1
    runtime: python
    api_version: 1

    handlers:
    - url: /pages/.*
      script: yourapp/handlers/pages.py

#### yourapp/handlers/pages.py

    import helipad

    class Page1(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page1')

    class Page2(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page2')

    main, application = helipad.app('/pages/', [
      ('page1/', Page1),
      ('page2/', Page2),
    ])

    if __name__ == "__main__":
      main()

### Sometimes the URL order doesn't matter...

#### app.yaml

    application: your-app-id
    version: 1
    runtime: python
    api_version: 1

    handlers:
    - url: /pages/.*
      script: yourapp/handlers/pages.py

#### yourapp/handlers/pages.py

    import helipad

    class Page1(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page1')

    class Page2(helipad.Handler):
      def get(self):
        self.response.out.write('Hello, helipad! This is Page2')

    main, application = helipad.app('/pages/', {
      'page1/': Page1,
      'page2/': Page2,
    })

    if __name__ == "__main__":
      main()

### Serving a static file

#### app.yaml

    application: your-app-id
    version: 1
    runtime: python
    api_version: 1

    handlers:
    - url: /about/
      script: yourapp/handlers/about.py

#### yourapp/handlers/about.py

    import helipad

    class StaticPage(helipad.Handler):
      def get(self):
        self.static('templates/about.html')
    
    # This tells helipad what module the path is relative to:
    helipad.root('yourapp')
    
    main, application = helipad.app(StaticPage)

    if __name__ == "__main__":
      main()

#### yourapp/tempates/about.html

    <html>
      <head>
        <title>About</title>
      </head>
      
      <body>
        <h1>Welcome to the about page!</h1>
        <p>Thanks for looking.</p>
      </body>
    </html>

### Serving a static file even easier!

#### app.yaml

    application: your-app-id
    version: 1
    runtime: python
    api_version: 1

    handlers:
    - url: /about/
      script: yourapp/handlers/about.py

#### yourapp/handlers/about.py

    import helipad

    main, application = helipad.root('yourapp').static('templates/about.html')

    if __name__ == "__main__":
      main()

#### yourapp/tempates/about.html

    <html>
      <head>
        <title>About</title>
      </head>
      
      <body>
        <h1>Welcome to the about page!</h1>
        <p>Thanks for looking.</p>
      </body>
    </html>

### Serving multiple static pages

#### app.yaml

    application: your-app-id
    version: 1
    runtime: python
    api_version: 1

    handlers:
    - url: /about/
      script: yourapp/handlers/about.py

#### yourapp/handlers/about.py

    import helipad

    main, application = helipad.root('yourapp').static('/about/', {
      '':          'templates/about.html',
      'company/':  'templates/about_company.html',
    })

    if __name__ == "__main__":
      main()

#### yourapp/tempates/about.html

    <html>
      <head>
        <title>About</title>
      </head>
      
      <body>
        <h1>Welcome to the about page!</h1>
        <p>Thanks for looking.</p>
      </body>
    </html>

#### yourapp/tempates/about_company.html

    <html>
      <head>
        <title>About the company</title>
      </head>
      
      <body>
        <h1>Our company</h1>
        <p>Our company is great! Thanks for looking.</p>
      </body>
    </html>

