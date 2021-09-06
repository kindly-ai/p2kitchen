import { gql, useQuery } from "@apollo/client";
import React, { ReactElement } from "react";

import { Machine } from "./Machine";
import classes from "./Today.module.css";

type TodayProps = { machines: Machine[] };

const GET_STATS = gql`
  {
    stats {
      litersToday
      litersYesterday
    }
  }
`;

const Summary = (): ReactElement => {
  const { data, loading } = useQuery(GET_STATS);
  if (loading) return <p>Loading</p>;

  const { litersToday, litersYesterday } = data.stats;
  const diffBrew = litersToday - litersYesterday;
  const moreOrLess = diffBrew >= 0 ? "more" : "less";
  return (
    <p className={classes.Summary}>
      Your team has brewed & consumed {litersToday}&nbsp;L coffee today, {Math.abs(diffBrew)}&nbsp;L {moreOrLess} than
      yesterday. Keep drinking!!
    </p>
  );
};

export const Today = ({ machines }: TodayProps): ReactElement => {
  return (
    <section>
      <h2>Today & now</h2>
      <p>Where to find the freshest coffee right now</p>
      {machines.map((machine: Machine) => {
        return <Machine key={machine.id} machine={machine} />;
      })}
      <Summary />
    </section>
  );
};
