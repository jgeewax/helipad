# Helipad!

## What the hell is helipad?

Helipad is a really simple "micro-framework" that makes it easy to do the stupid
stuff really quickly on Google AppEngine.

### ... Another one of these pieces of crap? You've got to be kidding.

As great as AppEngine is, it seemed like some stupid stuff (like the Hello World)
built with `webapp` was more verbose than it needed to be. I figured that there
must be a way to be a bit more terse without losing any clarity. This little file
has a few helpers that are just shorthand for things that you can do with `webapp`.

## Quickstart guide

Getting started with helipad is simple. Put the `.py` file in the directory where
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
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, helipad World!')

    main, application = helipad.app(HelloWorldHandler)

    if __name__ == "__main__":
      main()


