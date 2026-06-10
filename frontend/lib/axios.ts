import axios from "axios"

const apiClient = axios.create({
    baseURL: process.env.BASE_URL || "http://localhost:8002/api/v1",
    withCredentials: true,
    timeout: 30000,
    headers: {
        "Content-Type":"application/json",
    }
})

export default apiClient