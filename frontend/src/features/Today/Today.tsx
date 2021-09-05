import { gql, useQuery } from "@apollo/client";
import React, { ReactElement } from "react";

import "./Today.css";
import { Machine } from "./Machine";

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

const Today = (): ReactElement => {
  const { data, loading, error } = useQuery(GET_MACHINES);

  console.log("datas", data, "error", error);

  if (loading) return <p>Loading...</p>;
  const machines = data.machines;
  return (
    <section className="Status">
      <h2>Today & now</h2>
      <p>Where to find the freshest coffee right now</p>
      {machines.map((machine: Machine) => {
        return <Machine key={machine.id} machine={machine} />;
      })}

      <p className="Summary">
        Your team has brewed & consumed 13.5&nbsp;L coffee today, 4&nbsp;L less than yesterday. Keep drinking!!
      </p>
    </section>
  );
};
export default Today;
