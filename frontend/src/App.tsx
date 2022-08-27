import { useQuery, useSubscription } from "@apollo/client";
import React from "react";

import classes from "./App.module.css";
import { Stats } from "./features/Stats/Stats";
import { Today } from "./features/Today/Today";
import { ConnectToKitchenEventsDocument, MachinesDocument } from "./generated";

const App = () => {
  const { data: data, loading } = useQuery(MachinesDocument);
  const { data: eventsData, loading: eventsLoading } = useSubscription(ConnectToKitchenEventsDocument, {
    onSubscriptionData: ({ subscriptionData: { data, error, loading } }) => {
      // TODO: do something with this
      console.log("🔥 fresh datas", data, error, loading);
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
