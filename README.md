### Краткое описание

Курсовая работа по предмету "Программная инженерия". В ходе курсовой работы были созданы модель нейронной сети для распознавания рукописных цифр, сервер принимающий изображение и отправляющий ответом распознанное число и маломальский сайт для рисование этих цифр. 

Для работы были использованы фреймворки FastAPI и PyTorch. Более подробное описание и результаты можно посмотреть в отчете.

### Установка

Для начала надо установить python(если отсутствует) с официального сайта https://www.python.org/downloads/ . Также надо скачать git(если отсутствует) с официального сайта https://git-scm.com/downloads . Все следующие команды прописываются в cmd.

После проделать эти шаги:

```
git clone https://github.com/panikkuo/character-recognition.git
```

После перейти в эту папку и написать следующие команды

```
python -m venv venv

venv\Scripts\activate.bat

pip install -r requirements.txt
```

Если все получилось, то круто, если нет, можно сообщить мне о каких-то багах и плохо написанной инструкции.

### Запуск

Если не включено виртуальное окружение, то надо включить его:

```
venv\Scripts\activate.bat
```

Для запуска на своем локальном сервере можно написать(если нет, то поменять на свои необходимые):

```
uvicorn main:app  --reload --host 127.0.0.1 --port 8080
```

Для открытия сайта зайти на папку front и просто двойным кликом открыть Core.html и приступить исследованию. 