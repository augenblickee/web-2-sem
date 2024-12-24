// Общая функция для получения JSON
async function getJson(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `HTTP error ${response.status}`);
    }
    return response.json();
  }
  
  // Функция для отображения уведомлений (модальное окно или элемент)
  function showMessage(message, type = 'info') {
    alert(message)
  }
  
  let currentPage = 1;
  let totalPages = 1;
  let userId = null; // Добавим переменную для хранения user_id
  
  async function fillInitiativesList(page = 1) {
    try {
      const data = await getJson(`/rgz/rest-api/initiatives/?page=${page}`);
      const initiatives = data.initiatives;
      const tbody = document.getElementById('initiatives-list');
      tbody.innerHTML = '';
         // получаем user_id с сервера
       try {
           const  userData  = await getJson("/rgz/rest-api/user-data")
        if(userData && userData.user_id){
            userId = userData.user_id
        }
        else {
            userId = null
        }
       }
      catch (e){
           userId = null
       }
      initiatives.forEach(initiative => {
        const tr = document.createElement('tr');
          const voteButtons =  `
                  <button onclick="voteInitiative(${initiative.id}, 1)" ${initiative.user_vote === 1 ? 'disabled': ''}>За</button>
                  <button onclick="voteInitiative(${initiative.id}, -1)" ${initiative.user_vote === -1 ? 'disabled': ''}>Против</button>
               `;
  
        tr.innerHTML = `
                  <td>${initiative.id}</td>
                  <td>${initiative.title}</td>
                  <td>${initiative.content}</td>
                  <td>${new Date(initiative.created_at).toLocaleDateString()}</td>
                  <td>${initiative.score}</td>
                  <td>${initiative.author || "Неизвестно"}</td>
                   <td>${userId ? voteButtons : ''}</td>
                  
              `;
                tbody.appendChild(tr)
          });
          currentPage = data.page;
          totalPages = Math.ceil(data.total_count / data.per_page);
           updatePaginationButtons();
    } catch (error) {
        showMessage(`Ошибка загрузки списка инициатив: ${error.message}`, 'error');
    }
  }
  
  async function voteInitiative(initiativeId, voteValue) {
      try {
          await getJson(`/rgz/rest-api/vote/${initiativeId}/`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ vote: voteValue })
          });
          fillInitiativesList(currentPage); // Обновляем список
      } catch (error) {
           showMessage(error.message || 'Ошибка при голосовании', 'error');
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
          showMessage('Введите имя пользователя и пароль!', 'error');
          return;
      }
  
      try {
          await getJson('/rgz/rest-api/register', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ username, password }),
          });
          showMessage('Регистрация прошла успешно!', 'success');
          cancelRegister();
      } catch (error) {
        showMessage('Ошибка регистрации: ' + error.message, 'error');
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
      showMessage('Введите имя пользователя и пароль!', 'error');
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
          showMessage('Вход выполнен успешно!', 'success');
          cancelLogin();
         window.location.reload();
    } catch (error) {
      showMessage('Ошибка входа: ' + error.message, 'error');
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
        showMessage(`Ошибка при выходе: ${error.message}`, 'error');
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
      showMessage('Название и текст инициативы обязательны.', 'error');
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
          showMessage('Инициатива успешно добавлена!', 'success');
        closeAddInitiativeModal();
          fillInitiativesList();
        fillMyInitiativesList();
    } catch (error) {
       showMessage(error.message || 'Ошибка при добавлении инициативы.', 'error');
    }
  }
  
  async function fillMyInitiativesList() {
    try {
        const initiatives = await getJson('/rgz/rest-api/my-initiatives/');
        const tbody = document.getElementById('Myinitiatives-list');
         const userData = await getJson("/rgz/rest-api/user-data");
        tbody.innerHTML = '';
          if(initiatives.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">У вас нет своих инициатив</td></tr>'
          }
          else {
              initiatives.forEach(initiative => {
                const tr = document.createElement('tr');
                  let editButton;
                  let delButton;
                  if(userData && userData.user_id){
                         editButton = document.createElement('button');
                         editButton.innerText = 'Редактировать';
                         editButton.onclick = function() {
                            showEditInitiativeModal(initiative.id, initiative.title, initiative.content);
                        };
    
                         delButton = document.createElement('button');
                         delButton.innerText = 'Удалить';
                         delButton.onclick = function() {
                             deleteInitiative(initiative.id);
                         };
                  }
                  else{
                         editButton = document.createElement('button');
                           editButton.innerText = 'Редактировать';
                           editButton.disabled = true;
    
                        delButton = document.createElement('button');
                        delButton.innerText = 'Удалить';
                        delButton.disabled = true;
                  }
            
    
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
        }

    } catch (error) {
         showMessage(`Ошибка загрузки списка моих инициатив: ${error.message}`, 'error');
    }
}
  
  async function deleteInitiative(id) {
    if (confirm('Вы уверены, что хотите удалить эту инициативу?')) {
        try {
            await getJson(`/rgz/rest-api/initiatives/${id}/`, {
                method: 'DELETE'
            });
                showMessage('Инициатива удалена.', 'success');
                fillMyInitiativesList();
        } catch (error) {
            showMessage(error.message || 'Ошибка при удалении инициативы.', 'error');
        }
    }
  }
  
  let editingInitiativeId = null; // Добавили переменную для отслеживания редактирования
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
          showMessage('Название и текст инициативы обязательны.', 'error');
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
          showMessage('Инициатива успешно отредактирована!', 'success');
          closeEditInitiativeModal();
           fillMyInitiativesList();
          fillInitiativesList();
      } catch (error) {
         showMessage(error.message || 'Ошибка при редактировании инициативы.', 'error');
      }
  }