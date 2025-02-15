import axios from "axios";

const API_URL = "http://127.0.0.1:5000/";

export default {
  getData(endpoint) {
    return axios.get(`${API_URL}${endpoint}`)
      .then(response => {
        console.log("Axios Response Data:", response.data);  // 🔍 Debugging line
        return response.data;
      })
      .catch(error => {
        console.error("API GET Error:", error);
        throw error;
      });
  }
};
