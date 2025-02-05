let isMasked = false;
let originalValues = [];

document.addEventListener("DOMContentLoaded", function () {
    let elements = document.querySelectorAll('.user-info');
    elements.forEach(el => {
        originalValues.push(el.textContent);
    });
});

function toggleMask() {
    let elements = document.querySelectorAll('.user-info');
    elements.forEach((el, index) => {
        if (isMasked) {
            el.textContent = originalValues[index]; // asıl değerleri depolar
        } else {
            el.textContent = originalValues[index].replace(/[\d,.]+/, '***.**'); // sayıları *'a çevirir
        }
    });
    const x = document.getElementById("eyeBtn")
              if (x.classList.contains("fa-eye")){
                  x.classList.remove("fa-eye")
                  x.classList.add("fa-eye-slash")
              }else{
                  x.classList.remove("fa-eye-slash")
                  x.classList.add("fa-eye")
              }
    isMasked = !isMasked;
}


