// Общая функция для получения JSON
async function getJson(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `HTTP error ${response.status}`);
    }
    return response.json();
  }
  
let currentPage = 1;
let totalPages = 1;

async function fillInitiativesList(page = 1) {
  try {
    const data = await getJson(`/rgz/rest-api/initiatives/?page=${page}`);
    const initiatives = data.initiatives;
    const tbody = document.getElementById('initiatives-list');
    tbody.innerHTML = '';
      initiatives.forEach(initiative => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                    <td>${initiative.id}</td>
                    <td>${initiative.title}</td>
                    <td>${initiative.content}</td>
                    <td>${new Date(initiative.created_at).toLocaleDateString()}</td>
                    <td>${initiative.score}</td>
                    <td>${initiative.author || "Неизвестно"}</td>
                `;
              tbody.appendChild(tr)
        });
    
    currentPage = data.page;
    totalPages = Math.ceil(data.total_count / data.per_page);
     updatePaginationButtons();
  } catch (error) {
    alert(`Ошибка загрузки списка инициатив: ${error.message}`);
  }
}

function updatePaginationButtons() {
  const prevButton = document.getElementById('prev-page');
  const nextButton = document.getElementById('next-page');
    prevButton.disabled = currentPage <= 1;
    nextButton.disabled = currentPage >= totalPages;
}
function nextPage() {
    if (currentPage < totalPages) {
        fillInitiativesList(currentPage + 1);
    }
}

function prevPage() {
    if (currentPage > 1) {
        fillInitiativesList(currentPage - 1);
    }
}
  
  function showRegisterModal() {
    document.getElementById('register-modal').style.display = 'block';
  }
  
  function cancelRegister() {
    document.getElementById('register-modal').style.display = 'none';
  }
  
  async function register() {
      const username = document.getElementById('register-username').value;
      const password = document.getElementById('register-password').value;
  
      if (!username || !password) {
          alert('Введите имя пользователя и пароль!');
          return;
      }
  
      try {
          const data = await getJson('/rgz/rest-api/register', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ username, password }),
          });
          alert('Регистрация прошла успешно!');
          cancelRegister();
      } catch (error) {
          console.error('Ошибка:', error);
          alert('Ошибка регистрации: ' + error.message);
      }
  }
  
  
  function showLoginModal() {
    document.getElementById('login-modal').style.display = 'block';
  }
  
  function cancelLogin() {
    document.getElementById('login-modal').style.display = 'none';
  }
  
  
  async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
  
    if (!username || !password) {
      alert('Введите имя пользователя и пароль!');
      return;
    }
  
    try {
          await getJson('/rgz/rest-api/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ username, password }),
          });
          alert('Вход выполнен успешно!');
          cancelLogin();
          window.location.reload();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка входа: ' + error.message);
    }
  }
  
  
  
  async function logout() {
    try {
      await getJson('/rgz/rest-api/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      window.location.reload();
    } catch (error) {
      alert(`Ошибка при выходе: ${error.message}`);
    }
  }
  
  function showAddInitiativeModal() {
    document.getElementById('add-initiative-modal').style.display = 'block';
  }
  
  function closeAddInitiativeModal() {
    document.getElementById('add-initiative-modal').style.display = 'none';
  }
  
  async function addInitiative() {
    const title = document.getElementById('initiative-title').value;
    const content = document.getElementById('initiative-content').value;
  
    if (!title || !content) {
      alert('Название и текст инициативы обязательны.');
      return;
    }
    try {
      await getJson('/rgz/rest-api/initiatives/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ title, content })
      });
        alert('Инициатива успешно добавлена!');
        closeAddInitiativeModal();
        fillInitiativesList();
          fillMyInitiativesList();
    } catch (error) {
      alert(error.message || 'Ошибка при добавлении инициативы.');
    }
  }
  
  async function fillMyInitiativesList() {
      try {
          const initiatives = await getJson('/rgz/rest-api/my-initiatives/');
          const tbody = document.getElementById('Myinitiatives-list');
          tbody.innerHTML = '';
          initiatives.forEach(initiative => {
              const tr = document.createElement('tr');
  
              const editButton = document.createElement('button');
              editButton.innerText = 'Редактировать';
              editButton.onclick = function() {
                  editInitiative(initiative.id);
              };
  
              const delButton = document.createElement('button');
              delButton.innerText = 'Удалить';
              delButton.onclick = function() {
                  deleteInitiative(initiative.id);
              };
              tr.innerHTML = `
                  <td>${initiative.id}</td>
                  <td>${initiative.title}</td>
                  <td>${initiative.content}</td>
                  <td>${new Date(initiative.created_at).toLocaleDateString()}</td>
                  <td>${initiative.score}</td>
                   <td></td>
              `;
              tr.lastElementChild.append(editButton);
              tr.lastElementChild.append(delButton);
             
              tbody.appendChild(tr);
          });
      } catch (error) {
          alert(`Ошибка загрузки списка моих инициатив: ${error.message}`);
      }
  }
  
  async function deleteInitiative(id) {
    if (confirm('Вы уверены, что хотите удалить эту инициативу?')) {
        try {
            await getJson(`/rgz/rest-api/initiatives/${id}/`, {
                method: 'DELETE'
            });
              alert('Инициатива удалена.');
                fillMyInitiativesList();
        } catch (error) {
            alert(error.message || 'Ошибка при удалении инициативы.');
        }
    }
  }

  
let editingInitiativeId = null; // Добавили переменную для отслеживания редактирования
async function fillMyInitiativesList() {
    try {
        const initiatives = await getJson('/rgz/rest-api/my-initiatives/');
        const tbody = document.getElementById('Myinitiatives-list');
        tbody.innerHTML = '';
        initiatives.forEach(initiative => {
            const tr = document.createElement('tr');

            const editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function() {
                showEditInitiativeModal(initiative.id, initiative.title, initiative.content);
            };

            const delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function() {
                deleteInitiative(initiative.id);
            };
            tr.innerHTML = `
                <td>${initiative.id}</td>
                <td>${initiative.title}</td>
                <td>${initiative.content}</td>
                <td>${new Date(initiative.created_at).toLocaleDateString()}</td>
                <td>${initiative.score}</td>
                 <td></td>
            `;
            tr.lastElementChild.append(editButton);
            tr.lastElementChild.append(delButton);
           
            tbody.appendChild(tr);
        });
    } catch (error) {
        alert(`Ошибка загрузки списка моих инициатив: ${error.message}`);
    }
}


// Функция для отображения модального окна редактирования
function showEditInitiativeModal(id, title, content) {
    editingInitiativeId = id;
    document.getElementById('edit-initiative-title').value = title;
    document.getElementById('edit-initiative-content').value = content;
    document.getElementById('edit-initiative-modal').style.display = 'block';
}
// Функция для закрытия модального окна редактирования
function closeEditInitiativeModal() {
    document.getElementById('edit-initiative-modal').style.display = 'none';
    editingInitiativeId = null;
}

// Функция для отправки изменений на сервер
async function editInitiative() {
    const title = document.getElementById('edit-initiative-title').value;
    const content = document.getElementById('edit-initiative-content').value;

    if (!title || !content) {
        alert('Название и текст инициативы обязательны.');
        return;
    }

    try {
        await getJson(`/rgz/rest-api/initiatives/${editingInitiativeId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, content })
        });
        alert('Инициатива успешно отредактирована!');
        closeEditInitiativeModal();
         fillMyInitiativesList();
        fillInitiativesList();
    } catch (error) {
        alert(error.message || 'Ошибка при редактировании инициативы.');
    }
}