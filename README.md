# Игра "Пёс Павел"

Это текстовая ролевая игра про пса по имени Аркадий, который сражается с врагами и боссом Павлом.

## ВНИМАНИЕ: Эта ветка содержит значительные изменения в системе ввода/вывода!

**Подробное описание изменений:**

**Цель:**

Улучшить систему ввода/вывода, сделав её более гибкой, расширяемой и совместимой с различными окружениями (включая Skulpt, где может отсутствовать модуль `abc`).

**Что сделано:**

1. **Паттерн "Стратегия":** Вместо единого класса `IOHandler` с множеством условных операторов, теперь используются отдельные классы-стратегии для каждого режима вывода. Это улучшает читаемость, упрощает поддержку и облегчает добавление новых режимов.
2. **Базовый класс `BaseOutput`:** Определяет интерфейс для всех стратегий вывода (метод `print`).
3. **Конкретные стратегии:**
    *   `DelayedOutput`: Вывод текста с задержкой между символами (имитация печати).
    *   `InstantOutput`: Мгновенный вывод текста (как обычный `print`).
    *   `FileOutput`: Вывод в файл.
    *   `NullOutput`: Отключение вывода (ничего не выводится).
    *   `LoggerOutput`: Вывод через модуль `logging`.
4. **Класс `IOHandler`:**
    *   При инициализации читает конфигурационный файл `config.ini`.
    *   Использует словарь `output_strategies` для хранения доступных стратегий вывода.
    *   Выбирает текущую стратегию вывода на основе параметра `output_mode` в `config.ini`.
    *   Делегирует вывод текущей стратегии через метод `print`.
5. **Конфигурационный файл `config.ini`:**
    *   Позволяет настраивать режим вывода (`output_mode`), задержки (`delay`, `long_delay`) и другие параметры для конкретных стратегий.
    *   Содержит подробные комментарии, объясняющие доступные опции и инструкции по добавлению новых стратегий.
6. **Совместимость со Skulpt:** Изменения не используют модуль `abc` и полагаются на "утиную типизацию", что обеспечивает совместимость со Skulpt.
7. **Временное переключение режима вывода:** В методе `print` класса `IOHandler` появилась возможность временно переключить режим вывода с помощью параметра `output_mode`

**Как это работает:**

*   При запуске игры `IOHandler` читает настройки из `config.ini`.
*   В зависимости от значения параметра `output_mode` выбирается соответствующая стратегия вывода.
*   Все вызовы `io.print()`, `io.input()` и `io.delay_print()` в коде игры обрабатываются `IOHandler` и делегируются текущей стратегии.

**Обоснование выбора:**

Паттерн "Стратегия" был выбран для обеспечения гибкости и расширяемости системы ввода/вывода. Он позволяет легко добавлять новые режимы вывода без изменения основного кода `IOHandler`.

**Инструкции по тестированию:**

1. Переключитесь на ветку `feature/new-io-system`.
2. Запустите игру.
3. Проверьте, что вывод соответствует настройкам в `config.ini`.
4. Попробуйте изменить `output_mode` в `config.ini` на `instant`, `file`, `null`, `logger` и протестируйте, как меняется вывод.
    *   Для режима `file` необходимо раскомментировать и настроить параметры `file_path` и `append_mode`.
    *   Для режима `logger` необходимо раскомментировать и настроить параметры `logger_name` и `logging_level`.
5. Проверьте, что `delay_print` работает корректно с различными значениями задержки.
6. Проверьте, что если указан несуществующий способ вывода - это обрабатывается и не вызывает ошибок.

**Известные проблемы/ограничения:**

*   Пока нет стратегии для вывода с богатым форматированием (цвета, стили).

**Примеры использования различных стратегий вывода:**

*   **`delayed` (по умолчанию):**
    ```ini
    [IO]
    output_mode = delayed
    delay = 0.01
    long_delay = 2
    ```

*   **`instant`:**
    ```ini
    [IO]
    output_mode = instant
    ```

*   **`file`:**
    ```ini
    [IO]
    output_mode = file
    file_path = output.txt
    append_mode = true
    ```

*   **`null`:**
    ```ini
    [IO]
    output_mode = null
    ```

*   **`logger`:**
    ```ini
    [IO]
    output_mode = logger
    logger_name = game_log
    logging_level = DEBUG
    ```

## Как играть

1. Убедитесь, что у вас установлен Python 3.
2. Склонируйте репозиторий:

    ```bash
    git clone <ссылка на репозиторий>
    ```
3. Перейдите в директорию с игрой:

    ```bash
    cd <название директории>
    ```
4. **ВАЖНО: Переключитесь на ветку с новой системой ввода/вывода:**

    ```bash
    git checkout feature/new-io-system
    ```
5. Запустите игру:

    ```bash
    python arena.py
    ```

## Управление

*   Выберите действие, введя соответствующий номер и нажав Enter.

## Чит-коды

*   `PAVEL_BOG` - активирует чит-меню.

## Конфигурация

*   Настройки системы ввода/вывода находятся в файле `config.ini`.

## Лицензия

MIT License
