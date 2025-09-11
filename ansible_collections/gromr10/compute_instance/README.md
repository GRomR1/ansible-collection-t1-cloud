# T1 Cloud Ansible Collection

Данный проект представляет собой полноценную Ansible Collection для управления ресурсами в облачной платформе [Т1.Облаке](https://t1-cloud.ru/).

## Обзор

Коллекция `gromr10.compute_instance` предоставляет модули и плагины для автоматизации управления виртуальными машинами в T1 Cloud через REST API. Поддерживает полный жизненный цикл ВМ: создание, настройку, запуск, остановку и удаление.

## Структура проекта

```
ansible-collection-t1-cloud/
├── ansible_collections/gromr10/compute_instance/    # Основная коллекция
│   ├── galaxy.yml                                   # Метаданные коллекции
│   ├── README.rst                                   # Документация коллекции
│   ├── LICENSE                                      # Лицензия
│   ├── CHANGELOG.rst                                # История изменений
│   ├── CONTRIBUTING.rst                             # Руководство для разработчиков
│   ├── requirements.txt                             # Python зависимости
│   ├── plugins/                                     # Плагины Ansible
│   │   ├── modules/
│   │   │   └── t1_cloud_vm.py                      # Модуль управления ВМ
│   │   └── lookup/
│   │       └── t1_cloud_iam_token.py               # Плагин аутентификации
│   ├── meta/
│   │   └── runtime.yml                             # Метаинформация среды выполнения
│   ├── docs/                                       # Детальная документация
│   │   ├── t1_cloud_vm_module.rst
│   │   └── t1_cloud_iam_token_lookup.rst
│   └── examples/
│       └── create_vm.yml                           # Примеры использования
├── build_collection.sh                             # Скрипт сборки коллекции
├── PUBLISHING.md                                   # Руководство по публикации
└── README_COLLECTION.md                            # Этот файл
```

## Возможности

### Модули
- **t1_cloud_vm** - Управление виртуальными машинами
  - Создание, удаление, запуск, остановка ВМ
  - Настройка дисков (основной и дополнительные)
  - Сетевая конфигурация и публичные IP
  - Внедрение SSH ключей и cloud-init данных
  - Управление метками и группами безопасности

### Lookup плагины
- **t1_cloud_iam_token** - Получение токенов аутентификации
  - OAuth2 аутентификация через service account
  - Автоматическое обновление токенов
  - Кэширование для производительности

## Быстрый старт

### 1. Установка коллекции

Из Ansible Galaxy:
```bash
ansible-galaxy collection install gromr10.compute_instance
```

Или из исходников:
```bash
./build_collection.sh
ansible-galaxy collection install dist/gromr10-compute_instance-1.0.0.tar.gz
```

### 2. Пример использования

Создание ВМ

```yaml
---
- hosts: localhost
  collections:
    - gromr10.compute_instance

  vars:
    t1_api_token: "{{ lookup('t1_cloud_iam_token',
                     auth_method='service_account',
                     client_id='sa_proj-xxxx',
                     client_secret='your-secret') }}"

  tasks:
    - name: Создание ВМ
      t1_cloud_vm:
        api_token: "{{ t1_api_token }}"
        project_id: "proj-xxxxxxxxxxxx"
        name: "test-vm"
        image_id: "ubuntu-20.04"
        flavor_id: "small"
        subnet_id: "subnet-xxxxxxxxxxxx"
        disk_size: 50
        assign_public_ip: true
        ssh_keys:
          - "ssh-rsa AAAAB3NzaC1yc2E..."
        state: present
```

Управление состоянием ВМ

```yaml
# Остановить ВМ
- name: Stop VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-xxxxxxxxxx"
    name: "my-vm"
    state: stopped

# Запустить ВМ
- name: Start VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-xxxxxxxxxx"
    name: "my-vm"
    state: started

# Удалить ВМ
- name: Delete VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-xxxxxxxxxx"
    name: "my-vm"
    state: absent
```

### 3. Проверка установки

```bash
# Проверка документации модуля
ansible-doc gromr10.compute_instance.t1_cloud_vm

# Проверка lookup плагина
ansible-doc -t lookup gromr10.compute_instance.t1_cloud_iam_token
```

## Аутентификация

Коллекция поддерживает несколько способов аутентификации:

### 1. Прямое использование API токена
```yaml
- name: Создание ВМ с API токеном
  t1_cloud_vm:
    api_token: "your-api-token-here"
    # ... другие параметры
```

### 2. Service Account (рекомендуется)
```yaml
- name: Получение токена через Service Account
  set_fact:
    api_token: "{{ lookup('t1_cloud_iam_token',
                   auth_method='service_account',
                   client_id='sa_proj-xxxx',
                   client_secret='your-secret') }}"

- name: Создание ВМ
  t1_cloud_vm:
    api_token: "{{ api_token }}"
    # ... другие параметры
```

### 3. Файл с ключами
```yaml
- name: Использование файла ключей
  t1_cloud_vm:
    api_token: "{{ lookup('t1_cloud_iam_token',
                   auth_method='service_account',
                   key_file='/path/to/service-account.json') }}"
    # ... другие параметры
```

## Разработка

### Настройка окружения

1. Клонирование репозитория:
   ```bash
   git clone <repository-url>
   cd ansible-collection-t1-cloud
   ```

2. Создание виртуального окружения:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # или .venv\Scripts\activate  # Windows
   ```

3. Установка зависимостей:
   ```bash
   pip install ansible-core
   pip install -r ansible_collections/gromr10/compute_instance/requirements.txt
   ```

### Сборка коллекции

```bash
# Автоматическая сборка
./build_collection.sh

# Или ручная сборка
cd ansible_collections/gromr10/compute_instance
ansible-galaxy collection build --output-path ../../../dist --force
```

### Тестирование

```bash
# Локальная установка для тестирования
ansible-galaxy collection install dist/gromr10-compute_instance-1.0.0.tar.gz --force

# Тестирование документации
ansible-doc gromr10.compute_instance.t1_cloud_vm

# Запуск примеров
ansible-playbook ansible_collections/gromr10/compute_instance/examples/create_vm.yml --check
```

### Описание тестов

Проект включает несколько уровней тестирования:

1. **Юнит-тесты** (`test_vm_module.py`) - тестирование функций модуля
2. **Интеграционные тесты** - тестирование с реальным API (требуют токен).
   Необходимо расскоментировать вызов функции `test_vm_creation` в `test_vm_module.py`
3. **Плейбук-тесты** - полные сценарии использования

### Запуск тестов

```bash
# Юнит-тесты (без API вызовов)
python test_vm_module.py

# Тест проверки синтаксиса
ansible-playbook --syntax-check example-playbook.yml

# Плейбук тесты
export T1_CLOUD_PROJECT_ID="xxxxxxx"
export T1_CLOUD_CLIENT_ID="sa_proj-xxxxxxxxx"
export T1_CLOUD_CLIENT_SECRET="xxxxxxx"
ansible-playbook -i inventory.example example-playbook.yml
```

### Отладка

Включите детальный вывод Ansible:
```bash
# Максимальная детализация
ansible-playbook -vvv your-playbook.yml

# Только ошибки модуля
ansible-playbook --check your-playbook.yml
```

### Частые ошибки

1. **"Invalid VM name"**
   - Имя ВМ должно соответствовать паттерну `^[a-z][a-z0-9-]{1,61}[a-z0-9]$`
   - Начинается с буквы, содержит только строчные буквы, цифры и дефисы
   - Длина от 3 до 63 символов

2. **"API request failed"**
   - Проверьте правильность API токена
   - Убедитесь в доступности api.t1.cloud
   - Проверьте права токена на выполнение операций

3. **"VM not found"**
   - Убедитесь, что ВМ существует в указанном проекте
   - Проверьте правильность project_id
   - Проверьте точность написания имени ВМ

4. **"Operation timeout"**
   - Увеличьте `wait_timeout` для длительных операций
   - Проверьте статус операции в консоли T1.Cloud
   - Некоторые операции могут занимать больше времени

5. **"Subnet not found"**
   - Убедитесь, что subnet_id существует в проекте
   - Проверьте доступность подсети в выбранной зоне доступности

### Проверка подключения к API

Проверьте доступность API:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://api.t1.cloud/order-service/api/v1/projects/YOUR_PROJECT/orders"
```

### Мониторинг операций

Операции в T1.Cloud выполняются асинхронно. Вы можете отслеживать их через:
- Консоль T1.Cloud (раздел "Заказы")
- API endpoint для получения статуса заказа
- Логи Ansible при включенном параметре `wait: true`

## Публикация

### Подготовка к релизу

1. Обновление версии в `galaxy.yml`
2. Обновление `CHANGELOG.rst`
3. Тестирование сборки и функциональности
4. Создание git тега

### Публикация в Galaxy

Подробная инструкция в [PUBLISHING.md](PUBLISHING.md).

## Документация

- **README.rst** - Основная документация коллекции
- **docs/** - Детальная документация модулей и плагинов
- **examples/** - Примеры использования
- **CONTRIBUTING.rst** - Руководство для разработчиков

## Поддержка версий

- **Ansible Core**: 2.9.10 или выше
- **Python**: 3.6 или выше
- **T1 Cloud API**: v1

## Лицензия

[Apache License 2.0](./LICENSE)

## Поддержка

- **GitHub Issues**: Сообщения об ошибках и запросы функций
- **Документация T1 Cloud**: https://t1-cloud.ru/docs/

## Участие в разработке

Приглашаем к участию в развитии коллекции! См. [CONTRIBUTING.rst](ansible_collections/gromr10/compute_instance/CONTRIBUTING.rst) для подробностей.

### Планы развития

- Поддержка дополнительных сервисов T1 Cloud
- Модули управления сетями
- Модули управления хранилищем

## Авторы

- Руслан Гайнанов <rgainanov@inno.tech>
