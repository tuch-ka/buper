# Система резервного копирования
## Зависимости:
* Поддерживается только сиситема windows
* Необходима предварительная установка 7z (https://www.7-zip.org)
## Настройки:
* Создать файл settings.json (образец settings.json.example)
* Пути указываются с двойным слэшем `\\`, например `"c:\\base_1c\\trade"`
* После каждого параметра, кроме последнего, ставится запятая
* `ignore` является списком и запиывается следующим образом:
`["folder"]` или `["folder1", "folder2", "folder3"]`
* Обязательным для запуска является правильно указанный путь к архиватору `7z_exec`
## Описание параметров
+ Настройки резервного копирования
*  `source` - папка, из которой надо провести архивирование
*  `ignore` - папки, которые не надо включать в архив
*  `destination` - путь для сохранения архива
*  `count` - количество архивов, которые надо хранить. 0 - без ограничения
*  `lifetime` - количество дней, архивы старше которых надо удалять. 0 - без ограничения
+ Настройки архиватора
*  `7z_password` - пароль для архива
*  `7z_exec` - путь к исполняемому файлу 7z
+ Настройки почты для отправки лога
*  `mail_enable` - отправлять лог по электронной почте
*  `server` - сервер электронной почты
*  `port` - порт
*  `to_address` - адрес для отправки лога
*  `user` - пользователь почты
*  `password` - пароль от почты