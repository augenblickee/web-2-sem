function fillInitiativesList() {
    fetch('/rgz/rest-api/initiatives/')
    .then(function(data) {
        return data.json();
    })
    .then(function(initiatives) {
        let tbody = document.getElementById('initiatives-list');
        tbody.innerHTML = '';
        for(let i=0; i<initiatives.length; i++) {
            let tr = document.createElement('tr');

            let tdIni = document.createElement('td');
            let tdIniTxt = document.createElement('td');
            let tdData = document.createElement('td');
            let tdid = document.createElement('td');
            let tdScore = document.createElement('td');
            let tdAuthor = document.createElement('td'); // Добавляем колонку автора

            tdid.innerText = initiatives[i].id;
            tdIni.innerText = initiatives[i].title;
            tdIniTxt.innerText = initiatives[i].content;
            tdData.innerText = initiatives[i].created_at;
            tdScore.innerText = initiatives[i].score;
            tdAuthor.innerText = initiatives[i].author || "Неизвестно"; // Если автора нет, выводим "Неизвестно"

            tr.append(tdid);
            tr.append(tdIni);
            tr.append(tdIniTxt);
            tr.append(tdData);
            tr.append(tdScore);
            tr.append(tdAuthor);

            tbody.append(tr);
        }
    });
}

// Функция для отображения окна регистрации
function showRegisterModal() {
    document.getElementById('register-modal').style.display = 'block';
}

// Функция для скрытия окна регистрации
function cancelRegister() {
    document.getElementById('register-modal').style.display = 'none';
}

// Регистрация пользователя
function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    if (!username || !password) {
        alert('Введите имя пользователя и пароль!');
        return;
    }

    fetch('/rgz/rest-api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка HTTP: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Регистрация прошла успешно!');
                cancelRegister();
            } else {
                alert('Ошибка регистрации: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка регистрации.');
        });
}

// Функция для отображения окна входа
function showLoginModal() {
    document.getElementById('login-modal').style.display = 'block';
}

// Функция для скрытия окна входа
function cancelLogin() {
    document.getElementById('login-modal').style.display = 'none';
}


// Вход пользователя
function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    if (!username || !password) {
        alert('Введите имя пользователя и пароль!');
        return;
    }

    fetch('/rgz/rest-api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка HTTP: ' + response.status);
            }
            location.reload();
            return response.json();
            
        })
        .then(data => {
            if (data.success) {
                alert('Вход выполнен успешно!');
                cancelLogin();
            } else {
                alert('Ошибка входа: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка входа.');
        });
}

function logout() {
    fetch('/rgz/rest-api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            location.reload(); // Перезагружаем страницу после выхода
        } else {
            alert('Ошибка при выходе.');
        }
    });
}

function showAddInitiativeModal() {
    document.getElementById('add-initiative-modal').style.display = 'block';
}

function closeAddInitiativeModal() {
    document.getElementById('add-initiative-modal').style.display = 'none';
}

function addInitiative() {
    const title = document.getElementById('initiative-title').value;
    const content = document.getElementById('initiative-content').value;

    if (!title || !content) {
        alert('Название и текст инициативы обязательны.');
        return;
    }

    fetch('/rgz/rest-api/initiatives/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Инициатива успешно добавлена!');
            closeAddInitiativeModal();
            fillInitiativesList(); // Обновляем список инициатив
            location.reload(); 
        } else {
            alert(data.error || 'Ошибка при добавлении инициативы.');
        }
    });
}

function fillMyInitiativesList() {
    fetch('/rgz/rest-api/my-initiatives/')
        .then(response => response.json())
        .then(initiatives => {
            let tbody = document.getElementById('Myinitiatives-list');
            tbody.innerHTML = '';
            initiatives.forEach(initiative => {
                let tr = document.createElement('tr');

                let tdId = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdContent = document.createElement('td');
                let tdDate = document.createElement('td');
                let tdScore = document.createElement('td');
                let tdActions = document.createElement('td');
                
                tdId.innerText = initiative.id;
                tdTitle.innerText = initiative.title;
                tdContent.innerText = initiative.content;
                tdDate.innerText = initiative.created_at;
                tdScore.innerText = initiative.score;

                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                editButton.onclick = function() {
                    editInitiative(initiative.id);
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = function() {
                    deleteInitiative(initiative.id);
                };

                tdActions.append(editButton);
                tdActions.append(delButton);

                tr.append(tdId);
                tr.append(tdTitle);
                tr.append(tdContent);
                tr.append(tdDate);
                tr.append(tdScore);
                tr.append(tdActions);

                tbody.append(tr);
            });
        });
}

// Функция для удаления инициативы
function deleteInitiative(id) {
    if (confirm('Вы уверены, что хотите удалить эту инициативу?')) {
        fetch(`/rgz/rest-api/initiatives/${id}/`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Инициатива удалена.');
                fillMyInitiativesList(); // Обновляем список инициатив
            } else {
                alert(data.error || 'Ошибка при удалении инициативы.');
            }
        });
    }
}

