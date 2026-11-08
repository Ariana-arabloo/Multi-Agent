// src/services/api.js

const BASE_URL = 'http://localhost:8000/api/v1'; // آدرس پایه بک‌اند خودت رو چک کن

export const startNewProject = async (projectData) => {
  try {
    // ارسال درخواست POST به بک‌اند
    const response = await fetch(`${BASE_URL}/projects`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // اگر دیتایی مثل اسم پروژه داری اینجا بفرست، وگرنه یک آبجکت خالی
      body: JSON.stringify(projectData || {}), 
    });

    if (!response.ok) {
      throw new Error('خطا در شروع پروژه');
    }

    const data = await response.json();
    return data; // این دیتا باید شامل project_id باشه
  } catch (error) {
    console.error('Error starting project:', error);
    throw error;
  }
};