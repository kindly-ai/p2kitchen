import { ApolloClient, InMemoryCache } from "@apollo/client";

const API_URI = import.meta.env.VITE_API_URI || 'http://localhost:8000';

const client = new ApolloClient({
  uri: `${API_URI}/graphql`,
  cache: new InMemoryCache(),
});
export { client };
