import axios from "axios";
import { renewToken } from "./api";
import { useCookies } from 'vue3-cookies';

const { cookies } = useCookies();

axios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.request.status == 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      await renewToken();
      const access = await cookies.get("access_token")
      originalRequest.headers["Authorization"] = `Bearer ${access.value}`;
      return axios(originalRequest);
    }
    return Promise.reject(error);
  }
)

export default axios;