import React, { useState, useEffect } from "react";
import { View, Text, FlatList, StyleSheet, Image } from "react-native";
import Autocomplete from "react-native-autocomplete-input";
import { useNavigation } from "@react-navigation/native";

const restaurantsData = [
  {
    id: 1,
    name: "Example Restaurant 1",
    logo: require("../assets/logo.png"),
  },
  {
    id: 2,
    name: "Example Restaurant 2",
    logo: require("../assets/logo.png"),
  },
  {
    id: 3,
    name: "Example Restaurant 3",
    logo: require("../assets/logo.png"),
  },
  // Add more restaurants as needed
];

const RestaurantsScreen = () => {
  const [searchText, setSearchText] = useState("");
  const [filteredRestaurants, setFilteredRestaurants] =
    useState(restaurantsData);
  const navigation = useNavigation();

  useEffect(() => {
    filterRestaurants(searchText);
  }, [searchText]);

  const filterRestaurants = (text) => {
    const filteredData =
      text.length >= 2
        ? restaurantsData.filter((restaurant) =>
            restaurant.name.toLowerCase().includes(text.toLowerCase())
          )
        : [];
    setFilteredRestaurants(filteredData);
  };

  const handleSearch = (text) => {
    setSearchText(text);
  };

  const handleItemSelect = (item) => {
    navigation.navigate("RestaurantDetails", { restaurant: item });
  };

  const renderItem = ({ item }) => (
    <View style={styles.itemContainer}>
      <Image source={item.logo} style={styles.logo} resizeMode="contain" />
      <Text style={styles.itemText}>{item.name}</Text>
    </View>
  );

  const renderDropdownItem = ({ item, index, focused }) => (
    <TouchableOpacity
      style={[styles.dropdownItem, focused && styles.dropdownItemFocused]}
      onPress={() => handleItemSelect(item)}
    >
      <Image source={item.logo} style={styles.logo} resizeMode="contain" />
      <Text style={styles.dropdownItemText}>{item.name}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Autocomplete
        inputContainerStyle={styles.autocompleteContainer}
        data={filteredRestaurants.slice(0, 5)}
        defaultValue={searchText}
        onChangeText={handleSearch}
        placeholder="Search Restaurants"
        flatListProps={{
          keyExtractor: (item) => item.id,
          renderItem: renderDropdownItem,
        }}
        renderItem={renderDropdownItem}
        valueExtractor={(item) => item.name} // Extract the name property from the item object
        listItemProps={{
          onFocus: () => {
            // Handle focus event here (e.g., change color)
            console.log("Focused");
          },
        }}
      />
      <FlatList
        data={restaurantsData}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderDropdownItem}
        ItemSeparatorComponent={() => <View style={styles.separator} />}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  autocompleteContainer: {
    borderWidth: 0,
    marginBottom: 16,
  },
  itemContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
    backgroundColor: "#f2f2f2",
    padding: 12,
    borderRadius: 8,
  },
  dropdownItem: {
    flexDirection: "row",
    alignItems: "center",
    padding: 8,
  },
  dropdownItemFocused: {
    backgroundColor: "#f2f2f2", // Light gray background color for focused item
  },
  itemText: {
    fontSize: 16,
    marginLeft: 8,
  },
  dropdownItemText: {
    fontSize: 16,
    marginLeft: 8,
  },
  logo: {
    width: 30,
    height: 30,
  },
  separator: {
    height: 1,
    backgroundColor: "#ccc",
    marginVertical: 4,
  },
});

export default RestaurantsScreen;
