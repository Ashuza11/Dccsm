
const controlForm = document.getElementById('formControl');
const readBtn = document.getElementById('readBtn');
const writeBtn = document.getElementById('writeBtn');

console.log(controlForm);
console.log(readBtn);
console.log(writeBtn);

readBtn.addEventListener('click', handleReadClick);
writeBtn.addEventListener('click', handleWriteClick);

function handleReadClick() {
 console.log(controlForm);
}

function handleWriteClick() {
console.log(controlForm);
}






// function write_data(){
//     const form_command = document.getElementById('form_command');
//     const data_send = document.getElementById('data_send');
//     console.log(data_send.value);
//     form_command.action = "{% url 'protocole:write_data' %}";
//     form_command.submit(); 
// }