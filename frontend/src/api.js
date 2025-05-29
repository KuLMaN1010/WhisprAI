export async function getCoachingResponse(customer, agent) {
  const response = await fetch('http://localhost:5000/api/coach', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ customer, agent })
  });

  if (!response.ok) {
    throw new Error('API request failed');
  }

  const data = await response.json();
  return data;
}
