import React from "react";
import { Text } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Ionicons } from "@expo/vector-icons";
import { createStackNavigator } from "@react-navigation/stack";
import HomeScreen from "./main/src/HomeScreen";
import GroceryStoresScreen from "./main/src/GroceryStoresScreen";
import RestaurantsScreen from "./main/src/RestaurantsScreen";

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const HomeStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="Home"
      component={HomeScreen}
      options={{ headerShown: false }}
    />
  </Stack.Navigator>
);

const GroceryStoresStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="Grocery Stores"
      component={GroceryStoresScreen}
      options={{ headerShown: false }}
    />
  </Stack.Navigator>
);

const RestaurantsStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="Restaurants"
      component={RestaurantsScreen}
      options={{ headerShown: false }}
    />
  </Stack.Navigator>
);

const App = () => {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;

            if (route.name === "Home") {
              iconName = focused ? "home" : "home-outline";
            } else if (route.name === "GroceryStores") {
              iconName = focused ? "cart" : "cart-outline";
            } else if (route.name === "Restaurants") {
              iconName = focused ? "restaurant" : "restaurant-outline";
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: "tomato",
          tabBarInactiveTintColor: "gray",
          tabBarStyle: [
            {
              display: "flex",
            },
            null,
          ],
        })}
      >
        <Tab.Screen name="Home" component={HomeStack} />
        <Tab.Screen name="GroceryStores" component={GroceryStoresStack} />
        <Tab.Screen name="Restaurants" component={RestaurantsStack} />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

export default App;
