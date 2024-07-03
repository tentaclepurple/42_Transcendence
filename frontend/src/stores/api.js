import axios from '@/stores/axiosConfig'
import { useCookies } from 'vue3-cookies';

const { cookies } = useCookies();

export const renewToken = async () => {

  const refresh = cookies.get('refresh_token');

  if (!refresh)
      return ;

  const payload = {
      "refresh": refresh
  };

  const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + "/api/token/refresh/", payload);

  if (data && data.access) {
    cookies.set("access_token", data.access);
  } else {
    //this.$router("/login");
  }

}

export const deleteData = async (url, config = {}) => {

  try {
    const response = await axios.delete(url, config);
    return { data: response.data, error: null}
  } catch (error) {
    //console.error('Error fetching data:', error);
    return { data: null, error: error};
  }
};

// Wrapper for GET request
export const getData = async (url, config = {}) => {
  try {
    const response = await axios.get(url, config);
    return { data: response.data, error: null };
  } catch (error) {
    //console.error('Error fetching data:', error);
    return { data: null, error: error};
  }
};

// Wrapper for POST request
export const postData = async (url, data, config = {}) => {
  try {
    const response = await axios.post(url, data, config);
    return { data: response.data, error: null };
  } catch (error) {
    //console.error('Error posting data:', error);
    return { data: null, error: error};
  }
};