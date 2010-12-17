from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class index(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/header.html', locals()))
        self.response.out.write(template.render('templates/index_header.html', locals()))
        self.response.out.write(template.render('templates/index.html', locals()))
        self.response.out.write(template.render('templates/footer.html', locals()))

class about(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/header.html', locals()))
        self.response.out.write(template.render('templates/page_header.html', locals()))
        self.response.out.write(template.render('templates/about.html', locals()))
        self.response.out.write(template.render('templates/page_footer.html', locals()))
        self.response.out.write(template.render('templates/footer.html', locals()))

class resume(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/header.html', locals()))
        self.response.out.write(template.render('templates/page_header.html', locals()))
        self.response.out.write(template.render('templates/resume.html', locals()))
        self.response.out.write(template.render('templates/page_footer.html', locals()))
        self.response.out.write(template.render('templates/footer.html', locals()))

application = webapp.WSGIApplication(
                                     [('/', index), ('/resume', resume), ('/about', about)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

