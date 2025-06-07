import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
    });
  }

  async analyzeHouse(imageUri, latitude, longitude) {
    const formData = new FormData();
    formData.append('image', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'house-photo.jpg',
    });
    if (latitude && longitude) {
      formData.append('latitude', latitude.toString());
      formData.append('longitude', longitude.toString());
    }
    return this.client.post('/analyze-house', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async getPropertyDetails(propertyId) {
    return this.client.get(`/property/${propertyId}`);
  }
}

export default new ApiService(); 