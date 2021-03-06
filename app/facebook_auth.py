from tornado import web
from tornado import gen
from tornado import auth
import ujson as json


class FacebookAuth(web.RequestHandler, auth.FacebookGraphMixin):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_argument('error', None):
            raise web.HTTPError(
                    '500',
                    'Error: {0}\nReason: {1}\nDescription: {2}'.format(self.get_argument('error'), self.get_argument('error_reason','na'), self.get_argument('error_description', 'na'))
                    )
        if self.get_argument('code', None):
            access = yield self.get_authenticated_user(
                    redirect_uri= 'https://iamadatapoint.com/auth/facebook',
                    client_id=self.application.settings['facebook_oauth']['key'],
                    client_secret=self.application.settings['facebook_oauth']['secret'],
                    code=self.get_argument('code'))
            #Set Cookie, Eventually (change cookie_secret)
            print access
            self.redirect('https://iamadatapoint.com/test#test')
            return
        else:
            yield self.authorize_redirect(
                redirect_uri= 'https://iamadatapoint.com/auth/facebook',
                client_id=self.application.settings['facebook_oauth']['key'],
                client_secret=self.application.settings['facebook_oauth']['secret'],
                scope = ["public_profile","email","user_friends"])

            return
