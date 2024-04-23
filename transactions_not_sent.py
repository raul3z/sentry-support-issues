# encoding: utf-8
'''
:authors:
    | raul.catalina <raul.catalina@skydance.com>
:file: | sentry.sentry_support_test_02.py
:date: | 2024-04-09
:revision: | 2024-04-09
:summary: | Testing transactions not coming to Sentry
:copyright:
    | Copyright Skydance Animation Madrid S.L. 2024
    | The copyright to the computer program(s) herein is the property of Skydance Animation Madrid S.L..
    | The program(s) may be used and/or copied only with the written permission of Skydance Animation Madrid S.L.
        or in accordance with the terms and conditions stipulated in the agreement/contract under
        which the program(s) have been supplied.
'''

import os
import getpass
import sentry_sdk
from sentry_sdk.integrations.atexit import AtexitIntegration

DSN = '<YOUR-DSN-HERE>'


def hello(name):
    """ Dummy function to say Hello """
    print('Hello {}!'.format(name))


def init_sentry():
    """ Initializes Sentry """
    sentry_sdk.init(
        debug=True,
        dsn=DSN,
        max_breadcrumbs=100,
        environment=os.environ.get('ENVIRON'),
        traces_sample_rate=1.0,
        default_integrations=False,
        integrations=[
            AtexitIntegration()
        ],
    )
    sentry_sdk.set_user({'username': getpass.getuser()})


def send_transaction(name):
    """ Send a Sentry transaction """
    with sentry_sdk.start_transaction(name=name, op='test') as transaction:
        hello(name)
        transaction.hub.flush()


def main():
    """ Main function """
    init_sentry()
    for i in range(6):
        send_transaction('Sherlock.{}'.format(i + 1))
    send_transaction('Holmes')


if __name__ == '__main__':
    main()
