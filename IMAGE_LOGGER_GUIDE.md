# Enhanced ImageLogger Guide

## 🎯 Overview

Enhanced ImageLogger - это улучшенная версия инструмента для создания логов изображений с множественными вариантами хостинга, которая **НЕ использует ваш личный хостинг**.

## 🚀 Features

### ✅ **Новые возможности:**
- **Локальный HTTP сервер** - запуск сервера на вашем компьютере
- **Файловая система** - сохранение файлов локально
- **Пользовательский URL** - использование вашего собственного хостинга
- **ngrok туннель** - публичный доступ через ngrok
- **Улучшенный UI** - современный интерфейс с выбором опций
- **Автоматические скрипты** - создание bat-файлов для быстрого запуска

### 🔒 **Безопасность:**
- **Нет зависимости от личного хостинга**
- **Локальное выполнение**
- **Контроль над данными**

## 📋 Hosting Options

### 1. **Local HTTP Server (Рекомендуется)**
```
✅ Преимущества:
- Быстрая настройка
- Не требует внешних сервисов
- Полный контроль

⚠️ Ограничения:
- Доступен только в локальной сети
- Нужно держать программу открытой
```

### 2. **File System**
```
✅ Преимущества:
- Файлы сохраняются локально
- Можно загрузить на любой хостинг
- Полная независимость

⚠️ Ограничения:
- Нужно самостоятельно размещать файлы
- Требует веб-сервер
```

### 3. **Custom URL**
```
✅ Преимущества:
- Использование вашего хостинга
- Полный контроль над доменом
- Профессиональный вид

⚠️ Ограничения:
- Требует собственный хостинг
- Нужно загружать файлы вручную
```

### 4. **ngrok Tunnel**
```
✅ Преимущества:
- Публичный доступ
- Автоматическая настройка
- Не требует хостинга

⚠️ Ограничения:
- Требует установки ngrok
- URL меняется при перезапуске
- Ограничения бесплатного плана
```



## 🛠️ Installation

### Prerequisites
```bash
# Установка зависимостей
pip install requests colorama

# Для ngrok (опционально)
# Скачайте ngrok с https://ngrok.com/


```

### Quick Start
```bash
# Запуск через QuantumKit
python src/main.py

# Или напрямую
python src/utils/image_logger_enhanced.py
```

## 📖 Usage Guide

### Step 1: Запуск
1. Запустите QuantumKit
2. Выберите "ImageLogger"
3. Введите Discord webhook URL

### Step 2: Выбор хостинга
```
Choose hosting option:
1. Local HTTP Server (Recommended)
2. File System (Save locally)
3. Custom URL (Enter your own)
4. ngrok Tunnel (Requires ngrok)

```

### Step 3: Настройка

#### Option 1: Local Server
```
[*] Setting up local HTTP server...
[+] Local server started at http://localhost:8080
[+] URL: http://localhost:8080/image_AbCdEfGh.html
```

#### Option 2: File System
```
[+] File saved locally: generated_images/image_AbCdEfGh.html
[+] URL: file:///path/to/generated_images/image_AbCdEfGh.html
```

#### Option 3: Custom URL
```
[*] Enter your custom URL: https://yourdomain.com/
[+] URL: https://yourdomain.com/image_AbCdEfGh.html
```

#### Option 4: ngrok
```
[*] Checking for ngrok...
[+] ngrok found: 3.4.0
[*] Starting ngrok tunnel...
[+] URL: https://abc123.ngrok.io/image_AbCdEfGh.html
```



## 📁 File Structure

```
generated_images/
├── image_AbCdEfGh.html          # Основной файл логгера
├── open_image_AbCdEfGh.bat      # Скрипт для быстрого запуска
└── README.txt                   # Инструкции по использованию
```

## 🔧 Configuration

### Discord Webhook Setup
1. Создайте канал в Discord
2. Настройки канала → Интеграции → Вебхуки
3. Создайте новый вебхук
4. Скопируйте URL

### Local Server Configuration
```python
# Порт по умолчанию: 8080
# Можно изменить в коде:
self.port = 8080  # Измените на нужный порт
```

### ngrok Setup
```bash
# 1. Скачайте ngrok
# 2. Зарегистрируйтесь на ngrok.com
# 3. Добавьте authtoken
ngrok config add-authtoken YOUR_TOKEN

# 4. Запустите туннель
ngrok http 8080
```



## 📊 Data Collection

### Собираемые данные:
- **IP адрес** - реальный IP пользователя
- **User Agent** - информация о браузере
- **Платформа** - операционная система
- **Разрешение экрана** - размер экрана
- **Язык** - предпочитаемый язык
- **Часовой пояс** - временная зона
- **Временная метка** - точное время открытия

### Discord Embed Example:
```json
{
  "title": "🖼️ Image Logger Triggered",
  "description": "Someone opened the image logger!",
  "color": 0x00ff00,
  "fields": [
    {"name": "🌐 IP Address", "value": "192.168.1.1"},
    {"name": "🖥️ Platform", "value": "Win32"},
    {"name": "📱 Screen Resolution", "value": "1920x1080"},
    {"name": "🌍 Language", "value": "en-US"},
    {"name": "⏰ Timezone", "value": "Europe/Moscow"},
    {"name": "📅 Timestamp", "value": "2024-01-01T12:00:00Z"}
  ]
}
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Local Server не запускается
```bash
# Проверьте, не занят ли порт 8080
netstat -an | findstr :8080

# Измените порт в коде
self.port = 8081
```

#### 2. ngrok не найден
```bash
# Установите ngrok
# Скачайте с https://ngrok.com/
# Добавьте в PATH
```

#### 3. Playit.gg не найден
```bash
# Установите Playit.gg
# Скачайте с https://playit.gg/
# Или: winget install playit.gg
```

#### 3. Discord webhook не работает
```bash
# Проверьте URL webhook
# Убедитесь, что канал существует
# Проверьте права бота
```

#### 4. Файлы не создаются
```bash
# Проверьте права доступа к папке
# Убедитесь, что папка generated_images существует
```

### Debug Mode
```python
# Добавьте в код для отладки:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔄 Migration from Old Version

### Старая версия:
- Использовала ваш личный хостинг
- Ограниченные возможности
- Зависимость от внешних сервисов

### Новая версия:
- Множественные варианты хостинга
- Локальное выполнение
- Полная независимость

## 📈 Advanced Features

### Custom HTML Template
```html
<!-- Можно изменить HTML шаблон в коде -->
<style>
    /* Добавьте свои стили */
    body { background: linear-gradient(45deg, #ff6b6b, #4ecdc4); }
</style>
```

### Additional Data Collection
```javascript
// Добавьте дополнительные данные
const additionalInfo = {
    referrer: document.referrer,
    cookies: document.cookie,
    localStorage: JSON.stringify(localStorage)
};
```

### Custom Discord Embed
```python
# Измените формат Discord сообщения
embeds: [{
    "title": "Custom Title",
    "description": "Custom Description",
    "color": 0xff0000,  # Красный цвет
    "fields": [
        # Добавьте свои поля
    ]
}]
```

## 🛡️ Security Considerations

### Best Practices:
1. **Не используйте в незаконных целях**
2. **Получите согласие пользователей**
3. **Соблюдайте GDPR и другие законы**
4. **Защитите собранные данные**
5. **Используйте HTTPS для production**

### Legal Notice:
```
Этот инструмент предназначен только для образовательных целей.
Пользователи несут ответственность за свои действия.
Автор не несет ответственности за неправомерное использование.
```

## 📞 Support

### Getting Help:
1. Проверьте раздел Troubleshooting
2. Посмотрите логи в папке logs/
3. Запустите тест: `python test_image_logger.py`
4. Проверьте документацию

### Reporting Issues:
- Опишите проблему подробно
- Приложите логи ошибок
- Укажите версию Python и ОС
- Предоставьте шаги для воспроизведения

---

**Note**: Эта версия ImageLogger полностью независима и не использует личный хостинг автора. Все данные обрабатываются локально или на выбранном вами хостинге. 