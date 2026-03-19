// Auth Check
const token = localStorage.getItem('access');
const path = window.location.pathname;

if (!token && !path.endsWith('index.html')) {
    window.location.href = 'index.html';
} else if (token && path.endsWith('index.html')) {
    window.location.href = 'dashboard.html';
}

document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errEl = document.getElementById('loginError');

            try {
                const res = await fetch('http://127.0.0.1:8000/api/users/login/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                if (!res.ok) throw new Error("Invalid credentials");
                const data = await res.json();
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);

                try {
                    await ApiClient.request('/users/manage/');
                    localStorage.setItem('role', 'ADMIN_OR_LIB');
                } catch {
                    localStorage.setItem('role', 'MEMBER');
                }

                window.location.href = 'dashboard.html';
            } catch (err) {
                errEl.innerText = err.message;
                errEl.style.display = 'block';
            }
        });
    }

    if (document.getElementById('booksTable')) {
        document.getElementById('userRoleBadge').innerText = (localStorage.getItem('role') === 'ADMIN_OR_LIB') ? 'STAFF' : 'MEMBER';

        const logoutBtn = document.getElementById('logoutBtn');
        logoutBtn.addEventListener('click', () => {
            localStorage.clear();
            window.location.href = 'index.html';
        });

        loadBooks();
        loadTransactions();

        document.getElementById('searchInput').addEventListener('input', (e) => {
            loadBooks(e.target.value);
        });

        document.getElementById('refreshTxBtn').addEventListener('click', loadTransactions);

        const modal = document.getElementById('actionModal');
        document.getElementById('closeModal').addEventListener('click', () => modal.classList.add('hidden'));

        document.getElementById('confirmActionBtn').addEventListener('click', async () => {
            const bookId = document.getElementById('activeBookId').value;
            const txId = document.getElementById('activeTxId').value;
            const memberId = document.getElementById('memberIdInput').value;
            const actionMsg = document.getElementById('actionMsg');

            try {
                if (bookId) {
                    await ApiClient.request('/transactions/issue/', 'POST', { book_id: parseInt(bookId), member_id: parseInt(memberId) });
                } else if (txId) {
                    await ApiClient.request('/transactions/return/', 'POST', { transaction_id: parseInt(txId) });
                }
                modal.classList.add('hidden');
                loadBooks();
                loadTransactions();
            } catch (err) {
                actionMsg.innerText = err.message;
                actionMsg.style.color = 'var(--danger)';
            }
        });
    }
});

async function loadBooks(search = '') {
    const list = document.getElementById('booksList');
    try {
        const url = search ? `/books/?search=${encodeURIComponent(search)}` : '/books/';
        const data = await ApiClient.request(url);
        const books = data.results || data;

        list.innerHTML = '';
        const isStaff = localStorage.getItem('role') === 'ADMIN_OR_LIB';

        books.forEach(b => {
            const status = b.availability_status ? '<span class="status-available">Yes</span>' : '<span class="status-unavailable">No</span>';
            const actions = (isStaff && b.availability_status)
                ? `<button class="btn-secondary" onclick="openIssueModal(${b.id}, '${b.title}')">Issue</button>`
                : '-';

            list.innerHTML += `
                <tr>
                    <td>${b.id}</td>
                    <td>${b.title}</td>
                    <td>${b.author}</td>
                    <td>${b.category}</td>
                    <td>${status}</td>
                    <td>${actions}</td>
                </tr>
            `;
        });
    } catch (e) { console.error(e); }
}

async function loadTransactions() {
    const list = document.getElementById('transactionsList');
    try {
        const data = await ApiClient.request('/transactions/history/');
        const txs = data.results || data;
        list.innerHTML = '';
        const isStaff = localStorage.getItem('role') === 'ADMIN_OR_LIB';

        txs.forEach(t => {
            const actions = (isStaff && t.status === 'ISSUED')
                ? `<button class="btn-secondary" onclick="openReturnModal(${t.id}, '${t.book_details.title}')">Return</button>`
                : '-';

            list.innerHTML += `
                <tr>
                    <td>${t.id}</td>
                    <td>${t.book_details.title}</td>
                    <td>${t.member_details.id}</td>
                    <td>${t.status}</td>
                    <td>${t.issue_date}</td>
                    <td>${t.due_date}</td>
                    <td>${t.fine ? t.fine.amount : '0.00'}</td>
                    <td>${actions}</td>
                </tr>
            `;
        });
    } catch (e) { console.error(e); }
}

window.openIssueModal = function (bookId, title) {
    document.getElementById('activeBookId').value = bookId;
    document.getElementById('activeTxId').value = '';
    document.getElementById('modalTitle').innerText = 'Issue Book';
    document.getElementById('modalDesc').innerText = `Issuing "${title}"`;
    document.getElementById('memberInputGroup').classList.remove('hidden');
    document.getElementById('actionMsg').innerText = '';
    document.getElementById('actionModal').classList.remove('hidden');
}

window.openReturnModal = function (txId, title) {
    document.getElementById('activeTxId').value = txId;
    document.getElementById('activeBookId').value = '';
    document.getElementById('modalTitle').innerText = 'Return Book';
    document.getElementById('modalDesc').innerText = `Returning "${title}"`;
    document.getElementById('memberInputGroup').classList.add('hidden');
    document.getElementById('actionMsg').innerText = '';
    document.getElementById('actionModal').classList.remove('hidden');
}
