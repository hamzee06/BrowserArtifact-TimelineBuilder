const API_URL = 'http://127.0.0.1:8000';  // Your FastAPI backend URL

// export async function fetchHistory() {
//   const res = await fetch(`${API_URL}/history`);
//   return res.json();
// }
// src/services/api.  
// src/services/api.js
export const fetchHistory = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://127.0.0.1:8000/history', {
    method: 'POST',
     body: formData
  });

  if (!response.ok) {
    throw new Error('Failed to fetch history');
  }

  return await response.json();
};




export async function fetchCookies(file) {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/cookies`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("fetchCookies error:", error);
    return [];
  }
}

// export async function fetchLoginData(file) {
//   try {
//     const formData = new FormData();
//     formData.append("file", file);

//     const response = await fetch(`${API_URL}/logins`, {
//       method: "POST",
//       body: formData,
//     });

//     if (!response.ok) {
//       throw new Error(`HTTP error! Status: ${response.status}`);
//     }

//     const data = await response.json();
//     return Array.isArray(data) ? data : [];
//   } catch (error) {
//     console.error("fetchLoginData error:", error);
//     return [];
//   }
// }
// src/services/api.js
export const fetchLoginData = async (file) => {
  const formData = new FormData();
    formData.append("file", file);
  try {
    const response = await fetch('http://127.0.0.1:8000/logins', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch logins: ${errorText}`);
    }

    const result = await response.json();

if (Array.isArray(result)) {
  return result;   // backend already sends array
} else if (result && result.data) {
  return result.data; // in case backend wraps it
} else {
  console.warn('Unexpected response format:', result);
  return [];
}
  } catch (error) {
    console.error('Error in fetchLoginData:', error);
    throw error;
  }
};



export async function fetchRealTimeData() {
  const res = await fetch(`${API_URL}/realtime`);
  return res.json();
}
