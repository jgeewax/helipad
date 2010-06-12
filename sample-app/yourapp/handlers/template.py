import helipad

helipad.root('yourapp').template_root('static/templates/')

class TemplateHandler(helipad.Handler):
  def get(self):
    return self.template('template.html', {
      'person': self.request.get('person') or "Nobody!",
    })

main, application = helipad.app(TemplateHandler)

if __name__ == '__main__':
  main()
