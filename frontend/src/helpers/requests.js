import Cookies from "js-cookie";

const prod_mode = import.meta.env.PROD;
const baseUrl = prod_mode ? "" : "http://localhost:8000/";
/**
 * Send a post request to the backend
 */
export async function postRequest(url, data) {
  if (url.startsWith("/")) url = url.substring(1);
  try {
    const response = await fetch(baseUrl + url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      referrerPolicy: "no-referrer-when-downgrade",
      body: JSON.stringify(data),
    });
    if (response.status !== 200) {
      console.error(response);
      throw new Error("Error sending post request");
    }
    return response.json();
  } catch (e) {
    console.error(e);
    throw new Error("Error sending post request");
  }
}

export function getCSRFToken() {
  return Cookies.get("csrftoken");
}
