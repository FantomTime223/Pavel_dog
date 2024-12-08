import time
import sys
import configparser

class BaseOutput:
    """Базовый класс для всех стратегий вывода."""
    def print(self, text):
        raise NotImplementedError("Метод print должен быть реализован в дочернем классе")

class DelayedOutput(BaseOutput):
    """Вывод с задержкой."""
    def __init__(self, delay=0.01):
        self.delay = delay

    def print(self, text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.delay)
        print()

class InstantOutput(BaseOutput):
    """Мгновенный вывод."""
    def print(self, text):
        print(text)

class IOHandler:
    """
    Класс для обработки ввода и вывода с поддержкой различных стратегий вывода.
    """
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.output_mode = self.config.get("IO", "output_mode", fallback="delayed")
        self.delay = self.config.getfloat("IO", "delay", fallback=0.01)
        self.long_delay = self.config.getfloat("IO", "long_delay", fallback=2)

        # Словарь доступных стратегий вывода
        self.output_strategies = {
            "delayed": DelayedOutput(self.delay),
            "instant": InstantOutput(),
        }

        # Текущая стратегия вывода
        self.current_output = self.output_strategies.get(self.output_mode)
        if self.current_output is None:
            print(f"Ошибка: неизвестный режим вывода: {self.output_mode}. Используется delayed")
            self.current_output = DelayedOutput(self.delay)

    def print(self, text, output_mode=None):
        """
        Вывод текста с использованием выбранной стратегии вывода.

        Args:
            text: Текст для вывода.
            output_mode: Режим вывода. Если не указан, используется текущий режим из конфиг-файла.
        """
        if output_mode:
            # Временно переключаемся на указанный режим вывода
            current_output = self.output_strategies.get(output_mode)
        else:
            current_output = self.current_output

        current_output.print(text)

    def input(self, prompt=""):
        """
        Получение ввода от пользователя.

        Args:
            prompt: Приглашение для ввода (строка).

        Returns:
            Строка, введенная пользователем.
        """
        return input(prompt)

    def delay_print(self, text, delay=None):
        """
        Вывод текста с большой задержкой.

        Args:
            text: Текст для вывода.
            delay: Задержка перед выводом всего текста (в секундах).
                   Если не указана, используется задержка из конфигурации.
        """
        if delay is None:
            delay = self.long_delay
        time.sleep(delay) # задержка ПЕРЕД выводом
        self.print(text)

# Создаем экземпляр IOHandler, использующий конфигурационный файл.
io = IOHandler()