import { gql, useQuery } from "@apollo/client";
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

const App = (): ReactElement => {
  const { data, loading } = useQuery(GET_MACHINES);

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
