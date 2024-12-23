function fillInitiativeList() {
    fetch('/rgz/rest-api/initiatives/')
    .then(response => response.json())
    .then(initiatives => {
        let tbody = document.getElementById('initiative-list');
        tbody.innerHTML = '';
        initiatives.forEach(initiative => {
            let tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${initiative.id}</td>
                <td>${initiative.title}</td>
                <td>${initiative.content}</td>
                <td>${new Date(initiative.created_at).toLocaleDateString()}</td>
                <td>${initiative.score}</td>
                <td>
                    <button onclick="voteInitiative(${initiative.id}, 1)">За</button>
                    <button onclick="voteInitiative(${initiative.id}, -1)">Против</button>
                    <button onclick="editInitiative(${initiative.id})">Редактировать</button>
                    <button onclick="deleteInitiative(${initiative.id})">Удалить</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    });
}

function voteInitiative(id, vote) {
    fetch(`/rgz/rest-api/initiatives/${id}/vote`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({vote: vote})
    }).then(() => fillInitiativeList());
}

function addInitiative() {
    document.getElementById('initiative-id').value = '';
    document.getElementById('initiative-title').value = '';
    document.getElementById('initiative-content').value = '';
    showModal();
}

function sendInitiative() {
    const id = document.getElementById('initiative-id').value;
    const initiative = {
        title: document.getElementById('initiative-title').value,
        content: document.getElementById('initiative-content').value
    };
    const url = id ? `/rgz/rest-api/initiatives/${id}` : '/rgz/rest-api/initiatives/';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(initiative)
    }).then(() => {
        hideModal();
        fillInitiativeList();
    });
}

function deleteInitiative(id) {
    fetch(`/rgz/rest-api/initiatives/${id}`, {method: 'DELETE'})
    .then(() => fillInitiativeList());
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}
