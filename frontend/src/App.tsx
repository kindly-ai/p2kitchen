import React, { ReactElement } from "react";

import classes from "./App.module.css";
import Stats from "./Stats";
import { Today } from "./features/Today/Today";

const App = (): ReactElement => {
  return (
    <div className={classes.App}>
      <main className={classes.AppContainer}>
        <div className={classes.Panel}>
          <Today />
          <Stats />
        </div>
      </main>
    </div>
  );
};

export default App;
