import { useState, useEffect } from 'react';

function useDataUpload(apiUrl) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [responseData, setResponseData] = useState(null);

  const uploadData = async (dataToSend) => {
    setIsLoading(true);
    setError(null);
    setResponseData(null);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      });

      if (!response.ok) {
        throw new Error('Ошибка при отправке данных');
      }

      const responseData = await response.json();
      setResponseData(responseData);
      setIsLoading(false);
    } catch (error) {
      setError(error);
      setIsLoading(false);
    }
  };

  return { isLoading, error, responseData, uploadData };
}

export default useDataUpload;
