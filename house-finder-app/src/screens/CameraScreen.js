import React from 'react';
import { View } from 'react-native';
import CameraComponent from '../components/Camera';
import { useAppStore } from '../stores/appStore';
import ApiService from '../services/apiService';

export default function CameraScreen({ navigation }) {
  const { setCurrentPhoto, setLocation, setSearchResults, setLoading } = useAppStore();

  const handlePhotoTaken = async (photoData) => {
    setLoading(true);
    try {
      setCurrentPhoto(photoData.uri);
      setLocation(photoData.location);
      // Call API
      const response = await ApiService.analyzeHouse(
        photoData.uri,
        photoData.location?.latitude,
        photoData.location?.longitude
      );
      setSearchResults(response.data);
      navigation.navigate('Results');
    } catch (error) {
      console.error('Error analyzing house:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <CameraComponent onPhotoTaken={handlePhotoTaken} />
    </View>
  );
} 