# launch
# navigate
# scrape state
# perform action (set and click)

from aeoncloud import get_session_factory

aeon = get_session_factory()

session = aeon.get_session(request_body={
    'settings': {
        'aeon.platform.http.url': 'http://localhost:8001/api/v1/',
        'aeon.browser': 'Chrome',
        'aeon.protocol': 'https',
        'aeon.timeout': 10,
        'aeon.wait_for_ajax_responses': True,
        }
    })

session.execute_command('GoToUrlCommand', ['https://taskmgrclientdavid.apps.mia.ulti.io'])

session.execute_command('SetCommand', [{'type': 'css', 'value': "[data-automation='username-text-box']"}, "Text", "Test"])

session.execute_command('ClickCommand', [{'type': 'css', 'value': "[data-automation='login-button']"}])

session.quit_session()
