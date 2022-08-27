import { gql, useQuery, useSubscription } from "@apollo/client";
import React, { ReactElement } from "react";

import classes from "./App.module.css";
import { Stats } from "./features/Stats/Stats";
import { Today } from "./features/Today/Today";

const GET_MACHINES = gql`
  {
    machines {
      id
      name
      status
      avatarUrl
      litersTotal
      lastBrew {
        id
        status
        progress
        created
        modified
        brewer {
          userId
          realName
          displayName
          imageOriginal
          image48: image(size: 48)
        }
        reactions {
          id
          isCustomReaction
          reaction
          emoji
        }
      }
    }
  }
`;

const KITCHEN_EVENTS = gql`
  subscription {
    connectToKitchenEvents {
      type
      message
    }
  }
`;

const App = (): ReactElement => {
  const { data: data, loading } = useQuery(GET_MACHINES);
  const { data: eventsData, loading: eventsLoading } = useSubscription(KITCHEN_EVENTS);

  // TODO: do something with this
  console.log("🔥", eventsData, eventsLoading);

  if (loading) return <p>Loading...</p>;

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
