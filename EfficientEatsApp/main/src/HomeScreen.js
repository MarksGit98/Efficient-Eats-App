import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

const HomeScreen = () => {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.appName}>Efficient Eats</Text>
        {/* Replace the placeholder logo component with your actual logo */}
        <View style={styles.logoContainer}>
          <Ionicons name="logo-react" size={40} color="black" />
        </View>
      </View>
      <View style={styles.searchBar}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search"
          placeholderTextColor="#888"
        />
        <TouchableOpacity style={styles.searchButton}>
          <Ionicons name="search" size={24} color="white" />
        </TouchableOpacity>
      </View>
      <View style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Favorites</Text>
          {/* Replace this section with your favorites component */}
          <View style={styles.placeholder}>
            <Text>Favorite Items</Text>
          </View>
        </View>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Recently Viewed</Text>
          {/* Replace this section with your recently viewed component */}
          <View style={styles.placeholder}>
            <Text>Recently Viewed Items</Text>
          </View>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 20,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
  },
  appName: {
    fontSize: 20,
    fontWeight: "bold",
  },
  logoContainer: {
    width: 40,
    height: 40,
    backgroundColor: "#eee",
    justifyContent: "center",
    alignItems: "center",
  },
  content: {
    flex: 1,
    padding: 16,
  },
  section: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 8,
  },
  placeholder: {
    height: 100,
    backgroundColor: "#f0f0f0",
    justifyContent: "center",
    alignItems: "center",
  },
  searchBar: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#f0f0f0",
    padding: 8,
  },
  searchInput: {
    flex: 1,
    height: 40,
    backgroundColor: "white",
    borderRadius: 8,
    paddingHorizontal: 16,
    marginRight: 8,
  },
  searchButton: {
    backgroundColor: "tomato",
    borderRadius: 8,
    padding: 8,
  },
});

export default HomeScreen;
