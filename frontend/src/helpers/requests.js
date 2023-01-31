/**
 * Send a post request to the backend
 */
export async function postRequest(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    referrerPolicy: "no-referrer-when-downgrade",
    body: JSON.stringify(data),
  });
  return response.json();
}
