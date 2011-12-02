#!/usr/bin/env python

from oauthtwitter import OAuthApi
from settings import OAUTH_SETTINGS

twitter = OAuthApi(OAUTH_SETTINGS['consumer_key'], OAUTH_SETTINGS['consumer_secret'])
credenciales = twitter.getRequestToken()

print twitter.getAuthorizationURL(credenciales)

pin = input('INGRESA TU PIN: ')
access_token = twitter.getAccessToken(credenciales, pin)

print "OAuth Token: " + access_token['oauth_token']
print "OAuth Token Secret: " + access_token['oauth_token_secret']

