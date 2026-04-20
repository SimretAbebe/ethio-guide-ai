/**
 * API Utility for EthioGuide Frontend
 * Provides centralized access to the backend API base URL
 */

export const getBaseUrl = (): string => {
  // Use the environment variable, or fallback to localhost during development
  const url = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001";
  
  // Ensure no trailing slash
  return url.replace(/\/+$/, "");
};

/**
 * Helper to fetch with base URL automatically prepended
 */
export const fetchApi = async (endpoint: string, options?: RequestInit) => {
  const baseUrl = getBaseUrl();
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  
  const response = await fetch(`${baseUrl}${cleanEndpoint}`, options);
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  
  return response.json();
};
