import { ApolloProvider } from "@apollo/client";
import React from "react";
import { createRoot } from "react-dom/client";

import "./index.css";

import App from "./App";
import { client } from "./config";

const container = document.getElementById("root");
if (!container) {
  throw new Error("Missing #root element");
}
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  </React.StrictMode>
);
