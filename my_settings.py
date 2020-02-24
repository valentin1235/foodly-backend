DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'  # 아래와 같은 옵션을 줘야 각 모델의 table명을 동적으로 지정가능하다
        }
    }
}

SECRET_KEY = ""
