import apiClient from "./axios";

apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,

  (error) => {
    const status = error.response?.status;


    if (error.response?.status === 401) {
      window.location.href = "/login"
    }

    if (status === 403) {
      window.location.href = "/dashboard";
    }

    return Promise.reject(error);
  }
);