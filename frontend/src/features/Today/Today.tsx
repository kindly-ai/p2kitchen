import React, { ReactElement } from "react";

import { Machine } from "./Machine";
import classes from "./Today.module.css";

type TodayProps = { machines: Machine[] };

export const Today = ({ machines }: TodayProps): ReactElement => {
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
