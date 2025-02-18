import axios from "axios";

const API_URL = "http://127.0.0.1:5000/";

export default {
  // GET request
  getData(endpoint) {
    return axios
      .get(`${API_URL}${endpoint}`)
      .then((response) => {
        console.log("Axios Response Data (GET):", response.data); // Debugging line
        return response.data;
      })
      .catch((error) => {
        console.error("API GET Error:", error);
        throw error;
      });
  },

  // POST request
  postData(endpoint, payload) {
    return axios
      .post(`${API_URL}${endpoint}`, payload)
      .then((response) => {
        console.log("Axios Response Data (POST):", response.data); // Debugging line
        return response.data;
      })
      .catch((error) => {
        console.error("API POST Error:", error.response?.data || error.message);
        throw error;
      });
  },

  // DELETE request
  deleteData(endpoint) {
    return axios
      .delete(`${API_URL}${endpoint}`)
      .then((response) => {
        console.log("Axios Response Data (DELETE):", response.data); // Debugging line
        return response.data;
      })
      .catch((error) => {
        console.error("API DELETE Error:", error.response?.data || error.message);
        throw error;
      });
  }
};