import React, { ReactElement } from "react";

import Stats from "./Stats";
import "./App.css";
import Today from "./Today";

const App = (): ReactElement => {
  return (
    <div className="App">
      <main className="App-container">
        <div className="Panel">
          <Today />
          <Stats />
        </div>
      </main>
    </div>
  );
};

export default App;
