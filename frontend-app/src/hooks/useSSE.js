import { useState, useEffect } from 'react';

export const useSSE = (projectId) => {
  const [latestEvent, setLatestEvent] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('idle');

  useEffect(() => {
    if (!projectId) return;

    const sseUrl = `http://localhost:8000/api/v1/projects/${projectId}/stream`;
    const eventSource = new EventSource(sseUrl);

    eventSource.onopen = () => {
      console.log('✅ به استریم وصل شدیم!');
      setConnectionStatus('connected');
    };

    eventSource.onmessage = (event) => {
      try {
        const parsedData = JSON.parse(event.data);
        console.log('📩 رویداد جدید:', parsedData);
        setLatestEvent(parsedData);
      } catch (err) {
        console.error('خطا در خواندن دیتا:', err);
      }
    };

    eventSource.onerror = () => {
      console.error('❌ ارتباط قطع شد، در حال تلاش مجدد...');
      setConnectionStatus('error');
    };

    return () => {
      eventSource.close();
      setConnectionStatus('idle');
    };
  }, [projectId]);

  return { latestEvent, connectionStatus };
};