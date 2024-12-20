const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');

let isDrawing = false;
let lastX = 0;
let lastY = 0;

const offsetX = canvas.getBoundingClientRect().left + window.scrollX;
const offsetY = canvas.getBoundingClientRect().top + window.scrollY;

canvas.addEventListener('mousedown', function (e) {
    isDrawing = true;
    lastX = e.clientX - offsetX;
    lastY = e.clientY - offsetY;
});


canvas.addEventListener('mouseup', () => {
    isDrawing = false;
    ctx.beginPath();
});

canvas.addEventListener('mousemove', (event) => {
    if (!isDrawing) return;

    const x = event.clientX - offsetX;
    const y = event.clientY - offsetY;

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 10; 
    ctx.lineCap = 'round';
    ctx.stroke();

    lastX = x;
    lastY = y;
});

document.getElementById('sendButton').addEventListener('click', function () {
    let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    let matrix = [];
    const n = canvas.height;
    const m = canvas.width;

    for (let i = 0; i < n; i++) {
        let row = [];
        for (let j = 0; j < m; j++) {

            const color = imageData[(i * m + j) * 4 + 4];
            row.push(color);
        }
        matrix.push(row);
    }
    fetch('api/v1/upload-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ matrix })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Успех:', data);
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});