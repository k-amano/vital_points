import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const vitalPointsAPI = {
  getAll: () => client.get('/vital-points/'),
  getById: (id) => client.get(`/vital-points/${id}/`),
};

export const learningHistoryAPI = {
  getAll: () => client.get('/learning-history/'),
  getStatistics: () => client.get('/learning-history/statistics/'),
  getWeakPoints: () => client.get('/learning-history/weak_points/'),
};

export const quizSessionAPI = {
  startNew: () => client.post('/quiz-sessions/start_new_session/'),
  getCurrentQuestion: (sessionId) => client.get(`/quiz-sessions/${sessionId}/current_question/`),
  submitAnswer: (sessionId, data) => client.post(`/quiz-sessions/${sessionId}/submit_answer/`, data),
  pause: (sessionId) => client.post(`/quiz-sessions/${sessionId}/pause/`),
  resume: (sessionId) => client.post(`/quiz-sessions/${sessionId}/resume/`),
  complete: (sessionId) => client.post(`/quiz-sessions/${sessionId}/complete/`),
};

export default client;
