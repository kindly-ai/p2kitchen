import React from "react";

import type { MachinesQuery } from "../../generated";
import { BrewProgress } from "./BrewProgress";
import { BrewReactions } from "./BrewReactions";
import { Brewer } from "./Brewer";
import { StatusText } from "./StatusText";
import classes from "./Today.module.css";

type MachineProps = { machine: MachinesQuery["machines"][0] };

export const MachineDetails = ({ machine }: MachineProps) => {
  const { lastBrew } = machine;
  return (
    <div className={classes.MachineItem}>
      <img src={machine.avatarUrl} className={classes.MachineAvatar} alt="Machine avatar" />
      <div className={classes.Brew}>
        <h3>{machine.name}</h3>
        <div className={classes.BrewStatus}>
          <StatusText brew={lastBrew} />
        </div>
        <div>
          <BrewProgress brew={lastBrew} />
        </div>
        <Brewer brew={lastBrew} />
      </div>
      <BrewReactions brew={lastBrew} />
    </div>
  );
};
