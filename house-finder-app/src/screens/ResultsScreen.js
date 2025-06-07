import React from 'react';
import { View, Text, TouchableOpacity, Linking, StyleSheet } from 'react-native';
import { Card, Button } from 'react-native-elements';
import { useAppStore } from '../stores/appStore';

export default function ResultsScreen({ navigation }) {
  const { searchResults } = useAppStore();

  const openZillowLink = () => {
    if (searchResults?.property?.zillow_url) {
      Linking.openURL(searchResults.property.zillow_url);
    }
  };

  if (!searchResults) {
    return (
      <View style={styles.container}>
        <Text>No results found.</Text>
        <Button title="Back to Home" onPress={() => navigation.navigate('Home')} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Card>
        <Card.Title>Property Match Found!</Card.Title>
        <Card.Divider />
        <Text>Address: {searchResults.property.address}</Text>
        <Text>Price: ${searchResults.property.price?.toLocaleString()}</Text>
        <Text>Confidence: {Math.round(searchResults.confidence_score * 100)}%</Text>
        <Button
          title="View on Zillow"
          onPress={openZillowLink}
          buttonStyle={{ marginTop: 15 }}
        />
      </Card>
      <Button
        title="Take Another Photo"
        type="outline"
        onPress={() => navigation.navigate('Camera')}
        buttonStyle={{ marginTop: 20 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
}); 