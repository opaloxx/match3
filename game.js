let BLOCK_SIZE = 50;
const BOARD_SIZE = 10;
const SCREEN_SIZE = BLOCK_SIZE * BOARD_SIZE;
const SCREEN_COLOR = 'rgb(0, 0, 0)'; // Используйте строку для цвета
const SELECT_COLOR = 'rgb(255, 255, 255)'; // Используйте строку для цвета
const SELECT_WIDTH = BLOCK_SIZE / 10;
const INACTIVE_COLOR_COEF = 0.5;

// Цвета кружочков
const circleColors = [
    'rgb(255, 0, 0)',
    'rgb(0, 255, 0)',
    'rgb(0, 0, 255)',
    'rgb(255, 255, 0)',
    'rgb(255, 0, 255)',
    'rgb(0, 255, 255)'
];

function fillCanvas(color) {
    // Получение элемента canvas и его контекста
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // Задание цвета для заполнения
    ctx.fillStyle = color;

    // Заполнение холста цветом
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function getMousePos(canvas, event) {
    let rect = canvas.getBoundingClientRect();
    return {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    };
}

function mouseToBoard(mousePos) {
    let x = Math.floor(mousePos.x / BLOCK_SIZE);
    let y = Math.floor(mousePos.y / BLOCK_SIZE);
    return { x, y };
}

function drawBoard(ctx, board, pos, selected, active) {
    // Заполнение холста основным цветом
    fillCanvas(SCREEN_COLOR);
    //ctx.fillStyle = SCREEN_COLOR;
    //ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = 0; j < BOARD_SIZE; j++) {
            let color = board[i][j] !== null ? circleColors[board[i][j]] : SCREEN_COLOR;
            if (!active[i][j]) {
                // Преобразование цвета в более тёмный/светлый
                let rgba = color.replace(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)/, (_, r, g, b) => 
                    `rgba(${r * INACTIVE_COLOR_COEF}, ${g * INACTIVE_COLOR_COEF}, ${b * INACTIVE_COLOR_COEF})`
                );
                color = rgba;
            }

            // Отрисовка круга
            ctx.beginPath();
            ctx.arc(
                i * BLOCK_SIZE + BLOCK_SIZE / 2,
                j * BLOCK_SIZE + BLOCK_SIZE / 2,
                BLOCK_SIZE / 2,
                0,
                Math.PI * 2
            );
            ctx.fillStyle = color;
            ctx.fill();
        }
    }

    // Отрисовка выделения
    [pos, selected].forEach(p => {
        // console.log(p);
        if (p !== null && active[p.x][p.y]) {
            ctx.beginPath();
            ctx.arc(
                p.x * BLOCK_SIZE + BLOCK_SIZE / 2,
                p.y * BLOCK_SIZE + BLOCK_SIZE / 2,
                BLOCK_SIZE / 2,
                0,
                Math.PI * 2
            );
            ctx.strokeStyle = SELECT_COLOR;
            ctx.lineWidth = SELECT_WIDTH;
            ctx.stroke();
        }
    });
}



function changeColors(board) {
    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = 0; j < BOARD_SIZE; j++) {
            // Генерация случайного индекса цвета
            let colorIndex = Math.floor(Math.random() * circleColors.length);
            board[i][j] = colorIndex;
        }
    }
}

function match3(board, active) {
    let changed = false;

    // Проверка по горизонтали
    for (let i = 0; i < BOARD_SIZE; i++) {
        let cnt = 1;
        for (let j = 1; j < BOARD_SIZE; j++) {
            if (board[i][j] === board[i][j - 1] && board[i][j] !== null && active[i][j] && active[i][j - 1]) {
                cnt++;
                continue;
            }
            if (cnt >= 3) {
                changed = true;
                for (let k = j - cnt; k < j; k++) {
                    board[i][k] = null;
                }
            }
            cnt = 1;
        }
        if (cnt >= 3) {
            changed = true;
            for (let k = BOARD_SIZE - cnt; k < BOARD_SIZE; k++) {
                board[i][k] = null;
            }
        }
    }

    // Проверка по вертикали
    for (let j = 0; j < BOARD_SIZE; j++) {
        let cnt = 1;
        for (let i = 1; i < BOARD_SIZE; i++) {
            if (board[i][j] === board[i - 1][j] && board[i][j] !== null && active[i][j] && active[i - 1][j]) {
                cnt++;
                continue;
            }
            if (cnt >= 3) {
                changed = true;
                for (let k = i - cnt; k < i; k++) {
                    board[k][j] = null;
                }
            }
            cnt = 1;
        }
        if (cnt >= 3) {
            changed = true;
            for (let k = BOARD_SIZE - cnt; k < BOARD_SIZE; k++) {
                board[k][j] = null;
            }
        }
    }

    return changed;
}

function updateActive(board, active) {
    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = BOARD_SIZE - 1; j >= 0; j--) {
            active[i][j] = true;
            if (j < BOARD_SIZE - 1 && active[i][j + 1] === false) {
                active[i][j] = false;
            }
            if (board[i][j] === null) {
                active[i][j] = false;
            }
        }
    }
}

function fall(board, active) {
    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = BOARD_SIZE - 1; j > 0; j--) {
            if (!active[i][j]) {
                // Обмен значений между соседними ячейками
                [board[i][j], board[i][j - 1]] = [board[i][j - 1], board[i][j]];
            }
        }
        // Замена верхнего элемента новым случайным значением, если он неактивен
        if (!active[i][0]) {
            board[i][0] = Math.floor(Math.random() * circleColors.length);
        }
    }
}

function checkSwap(a, b) {
    return Math.abs(a.x - b.x) + Math.abs(a.y - b.y) === 1;
}

function resizeCanvas() {
    var canvas = document.getElementById('gameCanvas');
    var ctx = canvas.getContext('2d');  // Получение контекста canvas
    var maxSize = Math.min(window.innerWidth, window.innerHeight);

    canvas.width = maxSize;
    canvas.height = maxSize;

    // Обновление размера блока
    BLOCK_SIZE = maxSize / BOARD_SIZE;

    // Пересчет размеров кружочков и их положения
    // drawBoard(ctx, board, currentPos, selected, active); // Убедитесь, что эти переменные определены

}


function main() {
    resizeCanvas();
    // Игровое поле
    let board = [];
    let active = [];
    for (let i = 0; i < BOARD_SIZE; i++) {
        board.push(new Array(BOARD_SIZE).fill(0));
        active.push(new Array(BOARD_SIZE).fill(true));
    }

    changeColors(board);

    // Получение элемента canvas и контекста
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    // canvas.width = SCREEN_SIZE;
    // canvas.height = SCREEN_SIZE;
    
    let pos = null;

    canvas.addEventListener('mousemove', function(event) {
        let mousePos = getMousePos(canvas, event);
        let t = mouseToBoard(mousePos);
        if (t.x < BOARD_SIZE && t.x >= 0 && t.y >= 0 && t.y < BOARD_SIZE) {
            pos = t;
        }
        //console.log(pos); // Пример использования: вывод позиции в консоль
        // Дополнительный код для взаимодействия с игрой...
    });

    let selected = null;

    canvas.addEventListener('mousedown', function(event) {
        let mousePos = getMousePos(canvas, event);
        let pos = mouseToBoard(mousePos);

        if (!active[pos.x][pos.y]) {
            return;
        }

        if (selected === null) {
            selected = pos;
        } else {
            if (checkSwap(pos, selected)) {
                // Обмен элементов
                [board[pos.x][pos.y], board[selected.x][selected.y]] =
                    [board[selected.x][selected.y], board[pos.x][pos.y]];

                // Проверка на совпадения и возвращение элементов назад, если совпадений нет
                if (!match3(board, active)) {
                    [board[pos.x][pos.y], board[selected.x][selected.y]] =
                        [board[selected.x][selected.y], board[pos.x][pos.y]];
                }
            }
            selected = null;
        }
    });

    window.addEventListener('resize', resizeCanvas);

    let iteration = 0;

    // Функция обновления игры
    function update() {
        iteration++;
        // Получение позиции мыши (потребуется дополнительный код для этого)
        // let mousePos = getMousePos(canvas);
        // let pos = mouseToBoard(mousePos);

        // Обработка событий мыши (потребуется дополнительный код для этого)

        // Здесь должна быть логика игры...

        // Отрисовка доски
        match3(board, active);
        updateActive(board, active);
        if (iteration % 10 == 0) {
            fall(board, active);
            updateActive(board, active);
        }
        drawBoard(ctx, board, pos, selected, active);

        // Запрос на следующее обновление
        requestAnimationFrame(update);
    }

    // Начало цикла обновления
    requestAnimationFrame(update);
}

// Запуск игры
main();
