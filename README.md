# Публикация фотографий в сообществе Вконтакте 
Скрипт интегрируется с API [VK](https://vk.com/dev/manuals) и [xkcd](https://xkcd.com/json.html), скачивает комиксы и публикует их в сообщество Вконтакте. 

## Как установить  
На компьютере должен быть уже установлен Python3. Для запуска скрипта установите виртуальное окружение: 

``` 
python3 -m venv venv 
```

Затем активируйте виртуальное окружение (вариант для Windows):

``` 
venv\Scripts\activate 
```

Затем активируйте виртуальное окружение (вариант для Mac OS):

``` 
source venv/bin/activate
```

Используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей: 

```
pip install -r requirements.txt
``` 


Скрипт работает с переменными окружения для взаимодействия с API VK. Для успешной работы скрипта необходимо получить: client_id, group_id, access_token, записать их в .env файл. 

client_id — id приложения в настройках на странице разработчиков;

group_id — id сообщества, можно узнать [здесь](https://regvk.com/id/);

access_token — токен доступа до настроек страницы, его можно получить, запустив модуль get_token.py (потребует в качестве обязательного аргумента: client_id). После успешного получения прав доступа в адресной строке должен появиться URL с нужным токеном.

```
echo CLIENT_ID=токен > .env
``` 

```
echo GROUP_ID=токен > .env
``` 

```
echo VK_ACCESS_TOKEN=токен > .env
``` 

Запуск скрипта осуществляется в командной строке: 

```
python main.py
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org/modules/). 
