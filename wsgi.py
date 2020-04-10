from werkzeug.middleware.proxy_fix import ProxyFix

from app import make_app

application = make_app()
# ProxyFix is useful when we have a NGINX proxy and we want, for example, to have access to the requester ip easily
application.wsgi_app = ProxyFix(application.wsgi_app)

if __name__ == "__main__":
    application.run()
