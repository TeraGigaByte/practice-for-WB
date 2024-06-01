from flask import Flask, request, render_template
from simpleeval import SimpleEval
import logging

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Инициализируем SimpleEval для безопасной оценки выражений
simple_evaluator = SimpleEval()
simple_evaluator.functions = {}

# Настройка логирования, создаем лог-файл app.log для записи информации и ошибок
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/')
def index():
    # Рендерим шаблон index.html, передаем None для result по умолчанию
    return render_template('index.html', result=None)


@app.route('/calculate', methods=['POST'])
def calculate():
    # Получаем выражение из формы, удаляем лишние пробелы
    expression = request.form['expression'].strip()

    # Проверяем, что выражение не пустое
    if not expression:
        result = "Error: Expression cannot be empty"
        logging.error("Received an empty expression")
    else:
        try:
            # Оцениваем выражение
            result = simple_evaluator.eval(expression)
            logging.info(f"Expression evaluated: {expression} = {result}")
        except (SyntaxError, NameError) as e:
            # Обрабатываем ошибки синтаксиса и неправильных имен
            result = "Error: Invalid expression"
            logging.error(f"Invalid expression: {expression} with error {e}")
        except Exception as e:
            # Обрабатываем другие возможные ошибки
            result = f"Error: {str(e)}"
            logging.error(f"Failed to evaluate expression: {expression} with error {e}")

    # Рендерим шаблон index.html с результатом вычислений
    return render_template('index.html', result=result)


# Запускаем приложение в режиме отладки
if __name__ == '__main__':
    app.run(debug=True)
