import { useQuery } from "@apollo/client";
import React from "react";

import classes from "./App.module.css";
import { Stats } from "./features/Stats/Stats";
import { Today } from "./features/Today/Today";
import { MachinesDocument, MachineUpdateDocument } from "./generated";

const App = () => {
  const { data: data, loading, subscribeToMore } = useQuery(MachinesDocument);

  subscribeToMore({
    document: MachineUpdateDocument,
    updateQuery: (prev, { subscriptionData }) => {
      if (!subscriptionData.data) return prev;
      // overwrite all
      return {
        machines: subscriptionData.data.machineUpdate.machines,
      };
    },
  });

  if (loading || !data?.machines) return <p>Loading...</p>;

  return (
    <div className={classes.App}>
      <main className={classes.AppContainer}>
        <div className={classes.Panel}>
          <Today machines={data.machines} />
          <Stats machines={data.machines} />
        </div>
      </main>
    </div>
  );
};

export default App;
