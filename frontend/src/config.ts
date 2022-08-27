import { ApolloClient, InMemoryCache, split, HttpLink } from "@apollo/client";
import { GraphQLWsLink } from "@apollo/client/link/subscriptions";
import { getMainDefinition } from "@apollo/client/utilities";
import { createClient } from "graphql-ws";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const WS_API_URL = import.meta.env.VITE_API_URL || "ws://localhost:8000";

/** Make subscription operations use WS and everything else HTTP */
const link = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return definition.kind === "OperationDefinition" && definition.operation === "subscription";
  },
  new GraphQLWsLink(createClient({ url: `${WS_API_URL}/graphql` })),
  new HttpLink({ uri: `${API_URL}/graphql` })
);

const cache = new InMemoryCache();

const client = new ApolloClient({ link, cache });
export { client };
