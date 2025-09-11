# T1.Cloud Ansible Module

Ansible модуль для управления виртуальными машинами в [Т1.Облаке](https://t1-cloud.ru/).

## Возможности

- ✅ Создание виртуальных машин
- ✅ Удаление виртуальных машин
- ✅ Запуск/остановка/удаление ВМ
- ✅ Настройка дисков (основной и дополнительные)
- ✅ Настройка сети и публичных IP
- ✅ Настройка групп безопасности
- ✅ Cloud-init пользовательские данные
- ✅ SSH ключи
- ✅ Метки (labels)
- ✅ Ожидание завершения операций

## Требования

- Python 3.6+
- Ansible 2.9+
- Библиотеки: requests

## Архитектура проекта

```
ansible-module-t1-cloud/
├── plugins/                    # Ansible плагины
│   ├── modules/               # Основные модули
│   │   └── t1_cloud_vm.py    # Модуль для управления ВМ
│   └── lookup/               # Lookup плагины
│       └── t1_cloud_iam_token.py  # Получение IAM токенов
├── module_utils/             # Общие утилиты
│   └── t1_cloud.py          # Базовые функции для работы с API (backup)
├── docs/                    # Документация (создается при необходимости)
├── tests/                   # Тесты (создается при необходимости)
├── example-playbook.yml     # Примеры использования
├── inventory.example        # Пример файла инвентаря
├── ansible.cfg              # Конфигурация Ansible
├── test_vm_module.py        # Unit-Тесты модуля
├── requirements.txt         # Python зависимости
├── README.md                # Основная документация
└── LICENSE                  # Лицензия Apache 2.0
```

## Компоненты системы

### 1. Основные модули (`plugins/modules/`)

#### t1_cloud_vm.py
- **Назначение**: Управление виртуальными машинами в Т1.Облако
- **Функционал**:
  - Создание ВМ с настройкой дисков, сети, безопасности
  - Удаление ВМ
  - Управление состоянием (запуск/остановка/удаление)
  - Поддержка дополнительных дисков
  - Настройка публичных IP адресов
  - Управление SSH ключами и cloud-init
- **API**: Использует Order Service API для создания заказов на ВМ

### 2. Lookup плагины (`plugins/lookup/`)

#### t1_cloud_iam_token.py
- **Назначение**: Получение IAM токенов для аутентификации
- **Функционал**:
  - Аутентификация через сервисный аккаунт (JWT)
  - Автоматическое обновление токенов
- **API**: Использует IAM Service API

## API взаимодействие

### Основные API endpoints

1. **IAM Service**: `https://auth.t1.cloud/auth/realms/Portal/protocol/openid-connect/token`
   - Получение токенов аутентификации

2. **Order Service**: `https://api.t1.cloud/order-service/api/v1/`
   - Создание и управление заказами на ресурсы
   - Получение статуса операций
   - Управление виртуальными машинами

## Жизненный цикл операций

### Создание ресурса

```
1. Валидация параметров
2. Получение/проверка токена
3. Проверка существования ресурса
4. Создание заказа через API
5. Ожидание завершения операции
6. Возврат результата
```

## Быстрый старт

### Создание простой ВМ

```yaml
- name: Create VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-xxxxxxxxxx"
    name: "my-vm"
    description: "My test virtual machine"
    image_id: "d0179cb4-bfad-4b8f-836f-9cfc02143560"
    flavor_id: "3b259b39-6e73-41d5-b98e-b93c0bf31e95"
    subnet_id: "d0a5e4c0-1323-483d-8f5a-0e797a0fdd85"
    disk_size: 30
    state: present
```

### Управление состоянием ВМ

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

## Параметры модуля

### Обязательные параметры

| Параметр | Описание |
|----------|----------|
| `api_token` | API токен для аутентификации в T1.Cloud |
| `project_id` | ID проекта в T1.Cloud |
| `name` | Имя виртуальной машины (должно соответствовать паттерну `^[a-z][a-z0-9-]{1,61}[a-z0-9]$`) |

### Параметры для создания ВМ

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `description` | string | `""` | Описание ВМ |
| `image_id` | string | - | ID образа для создания ВМ |
| `image_name` | string | - | Имя образа (альтернатива image_id) |
| `flavor_id` | string | - | ID конфигурации ВМ (CPU/RAM) |
| `flavor_name` | string | - | Имя конфигурации ВМ |
| `region_id` | string | `"0c530dd3-eaae-4216-8f9d-9b5710a7cc30"` | ID региона |
| `region_name` | string | `"ru-central1"` | Имя региона |
| `availability_zone_id` | string | `"d3p1k01"` | ID зоны доступности |
| `availability_zone_name` | string | `"ru-central1-a"` | Имя зоны доступности |

### Настройка дисков

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `disk_size` | int | `10` | Размер загрузочного диска в ГБ |
| `disk_type_id` | string | `"076482c0-0367-4dee-a16f-2c6673a97f7f"` | ID типа диска |
| `disk_type_name` | string | `"dorado-sp07"` | Имя типа диска |
| `extra_disks` | list | `[]` | Дополнительные диски |

Пример дополнительного диска:
```yaml
extra_disks:
  - name: "data-disk"
    size: 100
    type_id: "cb4724f6-e53e-4632-ac78-f83c4332add3"
    type_name: "ceph_hdd"
```

### Настройка сети

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `subnet_id` | string | - | ID подсети (обязательно при создании) |
| `subnet_cidr` | string | `"10.128.0.0/24"` | CIDR подсети |
| `subnet_name` | string | `"default-ru-central1-a"` | Имя подсети |
| `assign_public_ip` | bool | `false` | Назначить публичный IP |
| `create_public_ip` | bool | `true` | Создать новый публичный IP |
| `public_ip_bandwidth` | int | `1000` | Пропускная способность в Мбит/с |
| `requested_ip` | string | - | Конкретный внутренний IP адрес |
| `security_groups` | list | `[]` | Список ID групп безопасности |

### Дополнительные настройки

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `ssh_keys` | list | `[]` | Список ID SSH ключей |
| `user_data` | string | `""` | Cloud-init скрипт (максимум 16384 байт) |
| `labels` | dict | `{}` | Метки ключ-значение |

### Управление состоянием

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `state` | string | `"present"` | Желаемое состояние: `present`, `absent`, `started`, `stopped` |
| `wait` | bool | `true` | Ожидать завершения операции |
| `wait_timeout` | int | `600` | Максимальное время ожидания в секундах |

## Примеры использования

### Создание ВМ с дополнительными дисками

```yaml
- name: Create VM with extra storage
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-xxxxxxxxxx"
    name: "storage-vm"
    description: "VM with additional storage"
    image_id: "d0179cb4-bfad-4b8f-836f-9cfc02143560"
    flavor_id: "3b259b39-6e73-41d5-b98e-b93c0bf31e95"
    subnet_id: "d0a5e4c0-1323-483d-8f5a-0e797a0fdd85"
    disk_size: 50
    extra_disks:
      - name: "app-data"
        size: 200
        type_id: "7ced5dc4-848a-4c02-bb76-8a3a9b7fff7f"
        type_name: "POD2_Average"
      - name: "logs"
        size: 100
        type_id: "cb4724f6-e53e-4632-ac78-f83c4332add3"
        type_name: "ceph_hdd"
    labels:
      environment: "production"
      team: "backend"
    state: present
```

### Создание ВМ с публичным IP и cloud-init

```yaml
- name: Create public VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-xxxxxxxxxx"
    name: "web-server"
    description: "Web server with public access"
    image_id: "d0179cb4-bfad-4b8f-836f-9cfc02143560"
    flavor_id: "3b259b39-6e73-41d5-b98e-b93c0bf31e95"
    subnet_id: "d0a5e4c0-1323-483d-8f5a-0e797a0fdd85"
    assign_public_ip: true
    public_ip_bandwidth: 2000
    user_data: |
      #cloud-config
      packages:
        - nginx
        - htop
      runcmd:
        - systemctl enable nginx
        - systemctl start nginx
        - echo "Server ready!" > /var/log/init.log
    ssh_keys:
      - "ssh-key-id-here"
    security_groups:
      - "security-group-id-here"
    state: present
```


## Архитектура модуля

Модуль состоит из следующих основных компонентов:

### T1CloudVM класс

Основной класс для взаимодействия с T1.Cloud API:
- `get_vm_by_name()` - поиск ВМ по имени
- `create_vm()` - создание новой ВМ
- `delete_vm()` - удаление ВМ
- `start_vm()`, `stop_vm()` - управление питанием
- `wait_for_operation()` - ожидание завершения операций

### Функции конфигурации

- `build_vm_config()` - построение конфигурации ВМ из параметров модуля
- `validate_name()` - валидация имени ВМ согласно требованиям T1.Cloud

### API Endpoints

Модуль использует следующие endpoints T1.Cloud API:
- `POST /order-service/api/v1/projects/{project_id}/orders` - создание заказов
- `GET /order-service/api/v1/projects/{project_id}/orders` - получение списка заказов
- `PATCH /order-service/api/v1/projects/{project_id}/orders/{id}/actions/{action}` - выполнение действий

## Возвращаемые значения

Модуль возвращает следующую информацию:

```yaml
vm:
  description: Информация о заказе ВМ
  type: dict
  sample:
    id: "15b92322-144f-4eec-9746-0d830f61647d"
    status: "success"
    created_at: "2025-09-01T10:08:11+03:00"
    updated_at: "2025-09-06T12:03:44+03:00"
    attrs:
      name: "my-vm"
      description: "My test VM"
      image:
        id: "d0179cb4-bfad-4b8f-836f-9cfc02143560"
        name: "osmax-astra-1-7-5-orel-gui-2025-05-19"
        os_distro: "astra"
      flavor:
        id: "3b259b39-6e73-41d5-b98e-b93c0bf31e95"
        name: "b5.large.2"
        vcpus: 2
        ram: 4096
      volumes_config:
        boot_volume:
          size: 30
          volume_type:
            name: "POD2_Average"

order_id:
  description: ID созданного/измененного заказа
  type: str
  sample: "15b92322-144f-4eec-9746-0d830f61647d"

changed:
  description: Было ли изменено состояние ВМ
  type: bool
```

## Запуск примеров

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

## Устранение неполадок

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

## Интеграция с другими инструментами

### Terraform

Модуль может работать совместно с Terraform:
```yaml
# Получить информацию о ресурсах из Terraform state
- name: Get subnet ID from Terraform
  shell: terraform output -json subnet_id
  register: tf_subnet

- name: Create VM using Terraform data
  t1_cloud_vm:
    subnet_id: "{{ (tf_subnet.stdout | from_json).value }}"
    # ... остальные параметры
```

### Динамические инвентари

```yaml
# Создание динамического инвентаря из созданных ВМ
- name: Add VM to inventory
  add_host:
    name: "{{ vm_result.vm.attrs.name }}"
    groups: web_servers
    ansible_host: "{{ vm_result.vm.attrs.network_configuration.requested_ip }}"
  when: vm_result is succeeded
```

### CI/CD интеграция

```yaml
# В GitLab CI/CD pipeline
deploy_vm:
  stage: deploy
  script:
    - ansible-playbook
        -e "vm_name=app-${CI_COMMIT_SHORT_SHA}"
        -e "image_tag=${CI_COMMIT_SHA}"
        deploy-vm.yml
```

## Производительность и масштабирование

### Параллельное выполнение

```yaml
# Создание нескольких ВМ параллельно
- name: Create multiple VMs
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "{{ project_id }}"
    name: "web-server-{{ item }}"
    # ... другие параметры
    state: present
  loop: "{{ range(1, 4) | list }}"  # web-server-1, web-server-2, web-server-3
  async: 600  # 10 минут на операцию
  poll: 0     # Не ждать завершения
  register: vm_jobs

- name: Wait for all VMs to be created
  async_status:
    jid: "{{ item.ansible_job_id }}"
  register: vm_results
  until: vm_results.finished
  retries: 60
  delay: 10
  loop: "{{ vm_jobs.results }}"
```

## Вклад в проект

### Планируемые модули

1. **t1_cloud_network.py** - управление сетями
2. **t1_cloud_security_group.py** - группы безопасности
3. **t1_cloud_image.py** - управление образами
4. **t1_cloud_snapshot.py** - снимки дисков
5. **t1_cloud_backup.py** - резервные копии

### Разработка

1. Форкните репозиторий
2. Создайте feature branch
3. Внесите изменения с тестами
4. Запустите тесты: `python test_vm_module.py`
5. Создайте Pull Request

### Стиль кода

- Следуйте PEP 8
- Используйте типизацию где возможно
- Документируйте функции в формате docstring
- Покрывайте новый код тестами

## Лицензия

[Apache License 2.0](./LICENSE)

## Поддержка

- **GitHub Issues**: для сообщения об ошибках и предложений
- **Документация T1.Cloud**: официальная документация API
- **Сообщество Ansible**: для общих вопросов по Ansible

## Авторы

Руслан Гайнанов <rgainanov@inno.tech>
