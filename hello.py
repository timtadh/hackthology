from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/header.html', locals()))
        self.response.out.write(template.render('templates/index.html', locals()))
        self.response.out.write(template.render('templates/footer.html', locals()))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

