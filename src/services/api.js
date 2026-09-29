const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

async function post(path, payload) {
  const response = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(data?.detail || 'We could not submit your request right now.');
  }
  return data;
}

export const submitBooking = payload => post('/api/bookings', Object.fromEntries(
  Object.entries(payload).map(([key, value]) => [
    key,
    value === '' && ['email', 'preferred_date', 'preferred_time', 'address', 'city', 'notes'].includes(key) ? null : value
  ])
));
export const submitContact = payload => post('/api/contact', payload);
