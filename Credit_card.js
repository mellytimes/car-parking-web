
/* script.js */
document.addEventListener('DOMContentLoaded', () => {
	const cardInput = document.getElementById('card');
	const cardType = document.getElementById('card-type');
	const previewNumber = document.getElementById('preview-number');
	const previewName = document.getElementById('preview-name');
	const previewExp = document.getElementById('preview-exp');
	const nameInput = document.getElementById('holder');
	const expInput = document.getElementById('exp');
	const qrModal = document.getElementById('qr-modal');
  
	cardInput.addEventListener('input', () => {
	  let value = cardInput.value.replace(/\D/g, '').replace(/(.{4})/g, '$1 ').trim();
	  cardInput.value = value;
	  previewNumber.textContent = value.padEnd(19, '*');
	  if (/^4/.test(value)) cardType.textContent = 'Visa';
	  else if (/^5[1-5]/.test(value)) cardType.textContent = 'Mastercard';
	  else cardType.textContent = '';
	});
  
	nameInput.addEventListener('input', () => {
	  previewName.textContent = nameInput.value.toUpperCase() || 'FULL NAME';
	});
  
	expInput.addEventListener('input', () => {
	  let v = expInput.value.replace(/[^0-9]/g, '').slice(0,4);
	  if (v.length >= 3) v = v.slice(0,2) + '/' + v.slice(2);
	  expInput.value = v;
	  previewExp.textContent = v || 'MM/YY';
	});
  
	document.getElementById('prompt-btn').addEventListener('click', () => {
	  qrModal.style.display = 'flex';
	});
	document.getElementById('close-qr').addEventListener('click', () => {
	  qrModal.style.display = 'none';
	});
  });