import { gql, useQuery } from "@apollo/client";
import React, { ReactElement } from "react";

import { Machine } from "./Machine";
import classes from "./Today.module.css";

const GET_MACHINES = gql`
  {
    machines {
      id
      name
      status
      avatarUrl
      lastBrew {
        id
        status
        progress
        created
        modified
        brewerSlackUsername
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

export const Today = (): ReactElement => {
  const { data, loading, error } = useQuery(GET_MACHINES);

  console.log("datas", data, "error", error);

  if (loading) return <p>Loading...</p>;
  const machines = data.machines;
  return (
    <section>
      <h2>Today & now</h2>
      <p>Where to find the freshest coffee right now</p>
      {machines.map((machine: Machine) => {
        return <Machine key={machine.id} machine={machine} />;
      })}

      <p className={classes.Summary}>
        Your team has brewed & consumed 13.5&nbsp;L coffee today, 4&nbsp;L less than yesterday. Keep drinking!!
      </p>
    </section>
  );
};
