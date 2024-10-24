const video = document.getElementById('video');
const shinyDot = document.getElementById('shiny-dot');

navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error('Error accediendo a la cámara: ', err);
    });

function animateDot() {
    shinyDot.style.transform = 'scale(1.5)';
    setTimeout(() => {
        shinyDot.style.transform = 'scale(1)';
    }, 200);
}

shinyDot.classList.add('moving');