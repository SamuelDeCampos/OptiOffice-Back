import os

HOST_IDS = {
    'dev': 'tsfwjfmweebjaxpkwjib',
    'prod': 'tgiokbxhgywidltduaxr',
    'tests': 'zswhbzgmqlxheljdborw'
}

HOST_KEYS = {
    'dev': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMTY4OTkwNCwiZXhwIjoxOTM3MjY1OTA0fQ.ksvqWHPZ0Vy-4--Bm5pn5gGV9ozn9jox_3GViqpm-u0',
    'prod': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMjkwMDc3MCwiZXhwIjoxOTM4NDc2NzcwfQ.7jcp1PCWN2ydz2jFa8XEzojqJ9XhqFy3L7CPZKY-MBM',
    'tests': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMjkwMjU3NCwiZXhwIjoxOTM4NDc4NTc0fQ.GX_PSbECS8goX2UX2Il-02pVWgt_LHVvDcLFpfvpU5U'
}

SECRET_KEY = 'MIIBOAIBAAJAUpbG4SwUwFTtKrU1qb5fKskK1Fio4vO1xiZoVJ1KQiZq+TFnzy39Ihrdl5bZb3Nm0U+/9irr5hD84sff0wli2QIDAQABAkABqYUxLPjx8gOf82u0Ed/K'


def get_config():
    print('has envvar:', os.environ.get('DEPLOY_MODE'))
    deploy_mode = os.getenv('DEPLOY_MODE', 'dev')

    print(deploy_mode)
    if deploy_mode not in HOST_IDS.keys():
        deploy_mode = 'dev'

    r = {
        'HOST_ID': HOST_IDS.get(deploy_mode),
        'HOST_KEY': HOST_KEYS.get(deploy_mode)
    }
    print(r)
    return r


DB_CONFIG = get_config()
