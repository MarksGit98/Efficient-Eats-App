import React, { useState } from "react";
import { View, Text, FlatList, TextInput, StyleSheet } from "react-native";

const groceryStoresData = [
  { id: 1, name: "Example Grocery Store 1" },
  { id: 2, name: "Example Grocery Store 2" },
  { id: 3, name: "Example Grocery Store 3" },
  // Add more grocery stores as needed
];

const GroceryStoresScreen = () => {
  const [searchText, setSearchText] = useState("");
  const [filteredGroceryStores, setFilteredGroceryStores] =
    useState(groceryStoresData);

  const handleSearch = (text) => {
    setSearchText(text);

    const filteredData = groceryStoresData.filter((store) =>
      store.name.toLowerCase().includes(text.toLowerCase())
    );
    setFilteredGroceryStores(filteredData);
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.searchInput}
        placeholder="Search Grocery Stores"
        value={searchText}
        onChangeText={handleSearch}
      />
      <FlatList
        data={filteredGroceryStores}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.itemContainer}>
            <Text style={styles.itemText}>{item.name}</Text>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  searchInput: {
    height: 40,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    paddingHorizontal: 12,
    marginBottom: 16,
  },
  itemContainer: {
    marginBottom: 8,
    backgroundColor: "#f2f2f2",
    padding: 12,
    borderRadius: 8,
  },
  itemText: {
    fontSize: 16,
  },
});

export default GroceryStoresScreen;
