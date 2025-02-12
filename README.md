# TChannels_Reowner 🚀

**TChannels_Reowner** - этот инструмент предназначен для автоматической перевязки Telegram-каналов и чатов с одного аккаунта на другой без возможно восстановления. 🛠

---

## 📋 О софте

**TChannels_Reowner** выполняет следующие действия:
1. Вход в Telegram-аккаунт. 🔑
2. Парсинг каналов/чатов, связанных с аккаунтом. 📋
3. Снятие администраторов с канала/чата. ❌
4. Приглашение вашего аккаунта и выдача ему прав администратора. ✅
5. Удаление аккаунта после успешной перевязки. 🗑

---

## 🛠 Требования

- **Python 3.10** (стабильная версия для работы с библиотекой `telethon`).

---

## 🚀 Установка

1. Скачайте проект и разместите его в удобной папке.
2. Установите зависимости, выполнив команду:
   ```bash
   pip install -r requirements.txt
3. Создать папку **tdatas**
---

## 🛡 Фикс банов Telegram-аккаунтов

1. Перейдите в папку:
```bash
C:\Users\ИМЯ_КОМПЬЮТЕРА\AppData\Local\Programs\Python\Python310\Lib\site-packages\opentele\tl\
```
2. Откройте файл telethon.py в любом текстовом редакторе.
3. Найдите строку 146 и замените строки 146-147 на следующие:
```bash
lang_code: str = "en",
system_lang_code: str = "en-US",
lang_pack: str = 'tdesktop',
```

---

## ⚙️ Настройка

1. Откройте файл config.json и настройте параметры:
```bash
{
  "subs_count": 1,               // Минимальное количество подписчиков для перевязки канала
  "to_invite_username": "USERTAG", // Ваш Telegram username (без @)
  "to_invite_id": USERID,    // Ваш Telegram ID (получить можно через @getmyid_bot)
  "dialogs": true                // Оставляем значение true
}
```
2. Поместите аккаунты в формате TDATA в папку tdatas.
3. Запуск проекта 
```bash
python main.py
```
---

## 🌐 Прокси (опционально)

Если вы настроили фикс банов Telegram-аккаунтов, прокси можно не использовать.
Однако, если требуется, добавьте прокси в формате:
```bash
IP:PORT:LOGIN:PASSWORD  
```
Тип прокси: SOCKS5.

---

## 💡 Примечания

1. Параметр в конфиге to_invite_username нужен для того, чтобы добавить ваш основной аккаунт в чат/канал и выдать админ права, если скрипт не может сделать этого (из-за приватности или флуд контроля), то ссылка на инвайт копируется в буфер обмена и вам нужно будет вручную вступить в телеграм канал
2. Если вы только получили сессию телеграм аккаунта, то нужно выждать 30 минут, чтобы выдавать админ права в чатах/каналах

--

## 🖼 Скрин работы софта


![screen](https://github.com/user-attachments/assets/2b0e9c56-be60-446d-8c56-20b3db85bd63)

