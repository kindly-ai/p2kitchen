import React, { ReactElement } from "react";

import { BrewProgress } from "./BrewProgress";
import { BrewReactions } from "./BrewReactions";
import { Brewer } from "./Brewer";
import { StatusText } from "./StatusText";

type MachineProps = { machine: Machine };

export const Machine = ({ machine }: MachineProps): ReactElement => {
  const { lastBrew } = machine;
  return (
    <div className="Machine-item">
      <img src={machine.avatarUrl} className="Machine-avatar" alt="Machine avatar" />
      <div className="Brew">
        <h3>{machine.name}</h3>
        <div className="Brew-status">
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
