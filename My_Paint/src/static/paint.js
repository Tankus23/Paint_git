// Выполняем по завершении загрузки страницы
    window.addEventListener("load", function onWindowLoad() {

        let canvasUrl;          //адрес картинки



        // Инициализируем переменные и генерируем палитру в элемент #palette
        generatePalette(document.getElementById("palette"));
        var canvas = document.getElementById("canvas");
        var context = canvas.getContext("2d");
        // переменные для рисования
        context.lineCap = "round";
        context.lineWidth = 8;

// Добавляем обработчик события отправки формы
  document.addEventListener('submit', function(event) {
    event.preventDefault(); // Отменяем отправку формы по умолчанию

    // Получаем значения полей формы
    const image_address = canvas.toDataURL("image/jpeg", 0.5);


    // Создаем объект FormData и добавляем значения полей формы
    const formData = new FormData();
    formData.append('image_address', image_address);


    // Отправляем запрос на сервер для аутентификации
    fetch("/paint/{profile_id}", {
    method: 'POST',
    headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    },
    body: JSON.stringify(image_address)
    })
    .then(function(response) {
      if (response.ok) {
        // Отображаем сообщение об успешном входе
        console.log(Ура)


      } else if (response.status === 400) {
        // Если получена ошибка 400 Bad Request
        response.json().then(function(data) {
          if (data.detail === 'LOGIN_BAD_CREDENTIALS') {
            // Если детализация ошибки "LOGIN_BAD_CREDENTIALS"
            // Отображаем сообщение об ошибке на странице
            const errorMessage = document.createElement('p');
            errorMessage.textContent = 'Неверный логин или пароль';
             console.log(Ура)
          }
        });
      } else {
        // Если получена другая ошибка, обрабатываем её соответствующим образом
        console.log('Ошибка:', response.status);
      }
    })
  });

        // вешаем обработчики на кнопки
        // очистка изображения
        document.getElementById("clear").onclick = function clear() {
          context.clearRect(0, 0, canvas.width, canvas.height);
        };

        // сохранение изображения
        document.getElementById("save").addEventListener('click', function(e) {
          canvasUrl = canvas.toDataURL("image/jpeg", 0.5);
          console.log(canvasUrl);
          const createEl = document.createElement('a');
          createEl.href = canvasUrl;
          createEl.download =  prompt("имя файла:  ");
          createEl.click();
          createEl.remove();
        });

       // загрузка изображения
        let fileInput = document.getElementById('images');
        fileInput.addEventListener('change', function(ev) {
           if(ev.target.files) {
              let file = ev.target.files[0];
              var reader  = new FileReader();
              reader.readAsDataURL(file);
              reader.onloadend = function (e) {
                  var image = new Image();
                  image.src = e.target.result;
                  image.onload = function(ev) {

                    let scale_factor = Math.min(canvas.width/image.width, canvas.height/image.height);

                    let newWidth = image.width * scale_factor;
                    let newHeight = image.height * scale_factor;
                    let x = (canvas.width/2) - (newWidth/2)
                    let y = (canvas.height/2) - (newHeight/2)

                    context.drawImage(image, x, y, newWidth, newHeight);
                 }
              }
           }
        });

        // На любое движение мыши по canvas будет выполнятся эта функция
        canvas.onmousemove = function drawIfPressed (e) {
          // в "e"  попадает экземпляр MouseEvent
          var x = e.offsetX;
          var y = e.offsetY;
          var dx = e.movementX;
          var dy = e.movementY;

          // Проверяем зажата ли какая-нибудь кнопка мыши
          // Если да, то рисуем
          if (e.buttons > 0) {
            context.beginPath();
            context.moveTo(x, y);
            context.lineTo(x - dx, y - dy);
            context.stroke();
            context.closePath();
          }
        };

        // генерируем палитру
        function generatePalette(palette) {
          // в итоге 5^3 цветов = 125
          for (var r = 0, max = 4; r <= max; r++) {
            for (var g = 0; g <= max; g++) {
              for (var b = 0; b <= max; b++) {
                var paletteBlock = document.createElement('div');
                paletteBlock.className = 'button';

                paletteBlock.addEventListener('click', function changeColor(e) {
                  context.strokeStyle = e.target.style.backgroundColor;
                });

                paletteBlock.addEventListener('contextmenu', function changeColor(e) {
                  canvas.style.background = e.target.style.backgroundColor;
                });

                paletteBlock.oncontextmenu = function(){return false;};

                paletteBlock.style.backgroundColor = (
                  'rgb(' + Math.round(r * 255 / max) + ", "
                  + Math.round(g * 255 / max) + ", "
                  + Math.round(b * 255 / max) + ")"
                );

                palette.appendChild(paletteBlock);
              }
            }
          }
        }
    });