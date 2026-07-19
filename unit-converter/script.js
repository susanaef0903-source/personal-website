// ============================================
// Unit converter: kilometers ↔ miles
// ============================================

// 1 kilometer = 0.621371 miles (the one fact the whole app is built on)
const MILES_PER_KM = 0.621371;

const amountInput = document.getElementById('amount');
const directionSelect = document.getElementById('direction');
const convertButton = document.getElementById('convert-btn');
const resultOutput = document.getElementById('result');

function convert() {
  const amount = parseFloat(amountInput.value);

  // If the box is empty or not a number, show a friendly message instead of NaN
  if (isNaN(amount)) {
    resultOutput.textContent = 'Please enter a number first.';
    resultOutput.classList.add('error');
    return;
  }
  resultOutput.classList.remove('error');

  const direction = directionSelect.value;
  let converted;
  let fromUnit;
  let toUnit;

  if (direction === 'km-to-mi') {
    converted = amount * MILES_PER_KM;
    fromUnit = 'km';
    toUnit = 'mi';
  } else {
    converted = amount / MILES_PER_KM;
    fromUnit = 'mi';
    toUnit = 'km';
  }

  // toLocaleString adds commas to big numbers; max 4 decimal places
  const formatted = converted.toLocaleString('en-US', { maximumFractionDigits: 4 });
  resultOutput.textContent = `${amount.toLocaleString('en-US')} ${fromUnit} = ${formatted} ${toUnit}`;
}

// Convert when the button is clicked...
convertButton.addEventListener('click', convert);

// ...or when the user presses Enter in the number box
amountInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    convert();
  }
});
