import { useQuery } from "@apollo/client";
import React from "react";

import { MachinesQuery, TodayStatsDocument } from "../../generated";
import { MachineDetails } from "./MachineDetails";
import classes from "./Today.module.css";

type TodayProps = { machines: MachinesQuery["machines"] };

const Summary = () => {
  const { data, loading } = useQuery(TodayStatsDocument);
  if (loading || !data?.stats) return <p>Loading...</p>;

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

export const Today = ({ machines }: TodayProps) => {
  return (
    <section>
      <h2>Today & now</h2>
      <p>Where to find the freshest coffee right now</p>
      {machines.map((machine) => {
        return <MachineDetails key={machine.id} machine={machine} />;
      })}
      <Summary />
    </section>
  );
};
