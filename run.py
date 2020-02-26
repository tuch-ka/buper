from check import check_settings
from buper import main

if __name__ == '__main__':
    # TODO: добавить проверку EMAIL_ENABLE
    if check_settings():
        main()
