from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <title>Калькулятор сложного процента</title>
</head>
<body>
    <h1>Калькулятор сложного процента</h1>
    <form method="post">
        Начальная сумма (основная сумма): <input type="number" name="principal" step="any" required><br>
        Годовая процентная ставка (%): <input type="number" name="rate" step="any" required><br>
        Количество лет: <input type="number" name="time" step="any" required><br>
        Частота начисления процента в году: <input type="number" name="times_per_year" value="1" required><br>
        <input type="submit" value="Рассчитать">
    </form>
    {% if error_message is not none %}
    <h2 style="color: red;" id="error_message">{{ error_message }}</h2>
    {% endif %}
    {% if result is not none %}
    <h2 id="result" >Итоговая сумма: {{ result }}</h2>
    {% endif %}
</body>
</html>
'''

def is_number(s):
    try:
        float(s)  # для проверки, может ли строка быть преобразована в число
        return True
    except ValueError:
        return False

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    error_message = None  # Добавление переменной для сообщения об ошибке
    if request.method == 'POST':
        principal = request.form['principal']
        rate = request.form['rate']
        time = request.form['time']
        times_per_year = request.form['times_per_year']
        if not (is_number(principal) and is_number(rate) and is_number(time) and is_number(times_per_year)):
            error_message = "Пожалуйста, убедитесь, что все введенные значения являются числами." 
        else:
            principal = float(request.form['principal'])
            rate = float(request.form['rate']) / 100
            time = float(request.form['time'])
            times_per_year = int(request.form['times_per_year'])
            if principal < 0 or rate < 0 or time < 0 or times_per_year < 1:
                error_message = "Все значения должны быть положительными, и частота начисления процента должна быть хотя бы 1."
            else:
                amount = principal * (1 + rate / times_per_year) ** (times_per_year * time)
                result = round(amount, 2)

    return render_template_string(TEMPLATE, result=result, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
