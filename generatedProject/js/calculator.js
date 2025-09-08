// Calculator Variables
let currentInput = '';
let currentOperator = null;
let previousInput = '';
let currentOperationState = 'initial'; // 'input', 'operator', 'result'

// Arithmetic Functions
function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b === 0) {
        alert("Error: Division by zero");
        return null;
    }
    return a / b;
}

// Operation Function
function performOperation() {
    const a = parseFloat(previousInput);
    const b = parseFloat(currentInput);
    let result = null;

    switch (currentOperator) {
        case '+':
            result = add(a, b);
            break;
        case '-':
            result = subtract(a, b);
            break;
        case '*':
            result = multiply(a, b);
            break;
        case '/':
            result = divide(a, b);
            break;
        default:
            return;
    }

    if (result !== null) {
        document.getElementById('display-screen').value = result;
        previousInput = result.toString();
        currentInput = '';
        currentOperator = null;
        currentOperationState = 'result';
    }
}

// Event Listeners
function initializeCalculator() {
    const digitButtons = document.querySelectorAll('.digit');
    const operatorButtons = document.querySelectorAll('.operator');
    const clearButton = document.querySelector('.clear');
    const displayScreen = document.getElementById('display-screen');

    // Digits event listener
    digitButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (currentOperationState === 'result') {
                previousInput = '';
                currentOperationState = 'input';
            }
            currentInput += button.textContent;
            displayScreen.value = currentInput;
        });
    });

    // Operators event listener
    operatorButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (button.textContent !== '=') {
                if (currentInput === '' && currentOperationState !== 'result') {
                    return;
                }

                if (currentOperator && currentInput) {
                    performOperation();
                }
                
                currentOperator = button.textContent;
                previousInput = currentInput;
                currentInput = '';
                currentOperationState = 'operator';
            } else {
                performOperation();
            }
        });
    });

    // Clear button event listener
    clearButton.addEventListener('click', () => {
        previousInput = '';
        currentInput = '';
        currentOperator = null;
        currentOperationState = 'initial';
        displayScreen.value = '';
    });
}

document.addEventListener('DOMContentLoaded', initializeCalculator);