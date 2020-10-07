# Система резервного копирования
## Зависимости:
* Поддерживаются сиситемы Windows и Linux
* __Необходима__ предварительная установка 7z (https://www.7-zip.org)
## Настройки:
* Без файла настроек будет выполнена попытка архивации текущего каталога
* Создать файл settings.json (образец settings.json.example)
* __Обязательным__ для работы является указанный путь к исполняемому файлу 7z,
если он отличается от стандартного
  * по умолчанию для Windows: `"c:\\Program Files\\7-Zip\\7z.exe"`
  * по умолчанию для Ubuntu: `"7z"`
* Пути указываются с двойным или обратным слэшем
  * пример для Windows: `"c:\\base_1c\\trade"`
  * пример для Ubuntu: `"/home/user/1c/trade"`
* После каждого параметра, кроме последнего, ставится запятая
* `ignore` является списком и запиывается следующим образом:
`["folder"]` или `["folder1", "folder2", "folder3"]`
## Описание параметров
+ Настройки резервного копирования
  *  `source` - папка, из которой надо провести архивирование
  *  `ignore` - папки и файлы, которые не надо включать в архив
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
+ Настройки логирования
  * `log_filename` - имя файла для сохранения логов
  * `log_folder` - папка для создания логов. в ходе работы программы лог будет перемещён в папку с архивом