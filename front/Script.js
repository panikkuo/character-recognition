const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');

let isDrawing = false
let lastX = 0
let lastY = 0

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
    ctx.lineWidth = 22; 
    ctx.lineCap = 'round';
    ctx.stroke();

    lastX = x;
    lastY = y;
});

function send_image(payload) {
    const xhr = new XMLHttpRequest();
    
    xhr.open("POST", "http://127.0.0.1:8080/upload-image", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            try {
                const response = JSON.parse(xhr.responseText);
                const predClass = document.getElementById('predicted-class-value');
                predClass.textContent = response.predicted_class;

                if (Array.isArray(response.probabilities) && response.probabilities.length === 10) {
                    for (let i = 0; i < response.probabilities.length; i++) {
                        const probElement = document.getElementById(`prob${i}`);
                        if (probElement) {
                            probElement.textContent = response.probabilities[i];
                        }
                    }
                } else {
                    console.error("Ответ сервера не содержит массива 'probabilities' из 10 элементов.");
                }
            } catch (error) {
                console.error("Ошибка при парсинге JSON:", error);
            }
        }
    };

    xhr.onerror = function () {
        console.log("Catched error!");
    }

    xhr.send(payload);
}

document.getElementById('sendButton').addEventListener('click', function () {
    let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    let matrix = [];
    const n = canvas.height;
    const m = canvas.width;
    for (let i = 0; i < n; i++) {
        let row = [];
        for (let j = 0; j < m; j++) {
            const color = imageData[(i * m + j) * 4 + 3];
            row.push(color);
        }
        matrix.push(row);
    }

    send_image(JSON.stringify({ matrix }));
});

document.getElementById('clearButton').addEventListener('click', function () {
    let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const n = canvas.height;
    const m = canvas.width;

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < m; j++) {
            imageData.data[(i * m + j) * 4 + 3] = 0;
        }
    }

    ctx.putImageData(imageData, 0, 0);
});