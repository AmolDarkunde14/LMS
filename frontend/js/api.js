const API_BASE = 'http://127.0.0.1:8000/api';

class ApiClient {
    static getToken() {
        return localStorage.getItem('access');
    }

    static async request(endpoint, method = 'GET', body = null) {
        const headers = { 'Content-Type': 'application/json' };
        const token = this.getToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const options = { method, headers };
        if (body) options.body = JSON.stringify(body);

        try {
            const res = await fetch(`${API_BASE}${endpoint}`, options);
            if (res.status === 401) {
                localStorage.clear();
                window.location.href = 'index.html';
                throw new Error("Unauthorized");
            }
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.error || data.detail || JSON.stringify(data) || 'Request failed');
            }
            if (res.status === 204) return null;
            return await res.json();
        } catch (e) {
            console.error("API Error:", e);
            throw e;
        }
    }
}
