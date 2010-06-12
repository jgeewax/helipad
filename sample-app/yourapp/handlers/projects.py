import helipad

class ProjectsHandler(helipad.Handler):
    def get(self, id):
        self.response.out.write("This is project #%s" % id)

main, application = helipad.app({
    '/projects/(\d+)/': ProjectsHandler,
})

if __name__ == '__main__':
    main()

