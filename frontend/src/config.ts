import { ApolloClient, InMemoryCache } from "@apollo/client";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const client = new ApolloClient({
  uri: `${API_URL}/graphql`,
  cache: new InMemoryCache(),
});
export { client };
