from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Variabel global untuk menyimpan hasil dan operasi
class Calculator:
    def __init__(self):
        self.display = "0"
        self.current_value = 0
        self.operator = None
        self.new_input = True
        self.history = []

calc = Calculator()

@app.route('/')
def index():
    """Halaman utama calculator"""
    return render_template('index.html', 
                          display=calc.display, 
                          history=calc.history)

@app.route('/input/<value>')
def input_value(value):
    """Handle input angka"""
    if calc.new_input:
        calc.display = value
        calc.new_input = False
    else:
        if calc.display == "0":
            calc.display = value
        else:
            calc.display += value
    return redirect(url_for('index'))

@app.route('/operator/<op>')
def operator(op):
    """Handle operator (+, -, *, /)"""
    try:
        calc.current_value = float(calc.display)
        calc.operator = op
        calc.new_input = True
    except:
        calc.display = "Error"
    return redirect(url_for('index'))

@app.route('/equals')
def equals():
    """Handle tombol equals (=)"""
    try:
        second_value = float(calc.display)
        first_value = calc.current_value
        op = calc.operator
        
        result = 0
        operation_str = f"{first_value} {op} {second_value}"
        
        if op == '+':
            result = first_value + second_value
        elif op == '-':
            result = first_value - second_value
        elif op == '*':
            result = first_value * second_value
        elif op == '/':
            if second_value != 0:
                result = first_value / second_value
            else:
                calc.display = "Error: Div by 0"
                return redirect(url_for('index'))
        
        # Format hasil
        if result == int(result):
            calc.display = str(int(result))
        else:
            calc.display = str(round(result, 8))
        
        # Simpan ke history
        history_entry = f"{operation_str} = {calc.display}"
        calc.history.insert(0, history_entry)
        if len(calc.history) > 10:
            calc.history.pop()
        
        calc.new_input = True
        calc.operator = None
        
    except Exception as e:
        calc.display = "Error"
    
    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    """Clear display (C)"""
    calc.display = "0"
    calc.new_input = True
    return redirect(url_for('index'))

@app.route('/clear-all')
def clear_all():
    """Clear semua (AC)"""
    calc.display = "0"
    calc.current_value = 0
    calc.operator = None
    calc.new_input = True
    return redirect(url_for('index'))

@app.route('/clear-history')
def clear_history():
    """Clear history"""
    calc.history = []
    return redirect(url_for('index'))

@app.route('/decimal')
def decimal():
    """Handle tombol decimal point"""
    if calc.new_input:
        calc.display = "0."
        calc.new_input = False
    elif "." not in calc.display:
        calc.display += "."
    return redirect(url_for('index'))

@app.route('/negate')
def negate():
    """Handle tombol +/-"""
    try:
        value = float(calc.display)
        calc.display = str(-value)
    except:
        pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
