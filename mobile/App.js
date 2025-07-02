import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList } from 'react-native';

export default function App() {
  const [servicios, setServicios] = useState([]);
  useEffect(() => {
    fetch('https://tu-backend.com/servicios')
      .then(r => r.json())
      .then(setServicios);
  }, []);

  return (
    <View style={{ padding: 20, marginTop: 40 }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Servicios</Text>
      <FlatList
        data={servicios}
        keyExtractor={item => `${item.id}`}
        renderItem={({ item }) => (
          <View style={{ marginBottom: 20 }}>
            <Text style={{ fontSize: 18 }}>
              {item.nombre} - ${item.precio}
            </Text>
            <Button
              title="Agendar"
              onPress={() => alert('Implementar navegación y APIs')}
            />
          </View>
        )}
      />
    </View>
  );
}
