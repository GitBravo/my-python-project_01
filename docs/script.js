let display = document.getElementById("display");
let currentInput = "0";
let previousInput = "";
let operator = "";

function updateDisplay() {
    display.value = currentInput;
}

function appendValue(value) {
    if (currentInput === "0" || currentInput === "Error") {
        currentInput = value;
    } else {
        currentInput += value;
    }
    updateDisplay();
}

function clearDisplay() {
    currentInput = "0";
    previousInput = "";
    operator = "";
    updateDisplay();
}

function backspace() {
    if (currentInput.length > 1) {
        currentInput = currentInput.slice(0, -1);
    } else {
        currentInput = "0";
    }
    updateDisplay();
}

function calculate() {
    if (previousInput === "" || operator === "") return;
    
    try {
        let result;
        let prev = parseFloat(previousInput);
        let curr = parseFloat(currentInput);
        
        switch (operator) {
            case "+":
                result = prev + curr;
                break;
            case "-":
                result = prev - curr;
                break;
            case "*":
                result = prev * curr;
                break;
            case "/":
                if (curr === 0) {
                    currentInput = "Error";
                    updateDisplay();
                    return;
                }
                result = prev / curr;
                break;
        }
        
        currentInput = String(result);
        previousInput = "";
        operator = "";
        updateDisplay();
    } catch (e) {
        currentInput = "Error";
        updateDisplay();
    }
}

document.addEventListener("keydown", function(e) {
    if (e.key >= "0" && e.key <= "9") {
        appendValue(e.key);
    } else if (e.key === "+" || e.key === "-" || e.key === "*" || e.key === "/") {
        if (previousInput === "") {
            previousInput = currentInput;
            operator = e.key;
            currentInput = "0";
        } else {
            calculate();
            previousInput = currentInput;
            operator = e.key;
            currentInput = "0";
        }
    } else if (e.key === "Enter") {
        calculate();
    } else if (e.key === "Backspace") {
        backspace();
    } else if (e.key === "Escape") {
        clearDisplay();
    } else if (e.key === ".") {
        appendValue(".");
    }
});