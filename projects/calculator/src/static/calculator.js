class CalculatorFrontEnd {
    constructor() {
        this.displayValue = '0';
        this.currentValue = null;
        this.currentOperation = null;
        this.waitingForSecondValue = false;

        this.displayElement = document.querySelector('.display-screen');
        this.bindEventListeners();
    }

    bindEventListeners() {
        document.querySelectorAll('.button-digit').forEach(button => {
            button.addEventListener('click', this.handleDigitClick.bind(this));
        });

        document.querySelectorAll('.button-operation').forEach(button => {
            button.addEventListener('click', this.handleOperationClick.bind(this));
        });

        document.querySelector('.button-clear').addEventListener('click', this.clearDisplay.bind(this));
    }

    handleDigitClick(event) {
        const value = event.target.textContent;
        if (this.waitingForSecondValue) {
            this.displayValue = value;
            this.waitingForSecondValue = false;
        } else {
            this.displayValue = this.displayValue === '0' ? value : this.displayValue + value;
        }
        this.updateDisplay();
    }

    handleOperationClick(event) {
        const operation = event.target.textContent;
        if (this.currentOperation && this.waitingForSecondValue) {
            this.currentOperation = operation;
            return;
        }
        if (this.currentValue == null && !isNaN(this.displayValue)) {
            this.currentValue = parseFloat(this.displayValue);
        } else if (this.currentOperation) {
            const result = this.performCalculation();
            this.displayValue = String(result);
            this.currentValue = result;
        }
        this.waitingForSecondValue = true;
        this.currentOperation = operation;
        this.updateDisplay();
    }

    performCalculation() {
        if (this.currentOperation && this.currentValue != null) {
            const secondValue = parseFloat(this.displayValue);
            switch (this.currentOperation) {
                case '+':
                    return this.currentValue + secondValue;
                case '-':
                    return this.currentValue - secondValue;
                case '*':
                    return this.currentValue * secondValue;
                case '/':
                    return this.currentValue / secondValue;
                default:
                    return secondValue;
            }
        }
        return parseFloat(this.displayValue);
    }

    clearDisplay() {
        this.displayValue = '0';
        this.currentValue = null;
        this.currentOperation = null;
        this.waitingForSecondValue = false;
        this.updateDisplay();
    }

    updateDisplay() {
        this.displayElement.textContent = this.displayValue;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    new CalculatorFrontEnd();
});
