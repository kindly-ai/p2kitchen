import { gql, useQuery } from "@apollo/client";
import { differenceInMinutes, formatDistanceToNow, parseISO } from "date-fns";
import React, { ReactElement } from "react";

import "./Today.css";
import bg from "./assets/bg.jpg";

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
type BrewReaction = {
  id: number;
  reaction: string;
  isCustomReaction: boolean;
  emoji: string;
};

type Brew = {
  id: number;
  status: string;
  progress: number;
  brewerSlackUsername: string;
  modified: string;
  created: string;
  reactions: BrewReaction[];
};
type Machine = {
  id: number;
  name: string;
  status: string;
  avatarUrl: string;
  lastBrew?: Brew;
  modified: string;
  created: string;
};

type MachineProps = { machine: Machine };
type StatusTextProps = { brew?: Brew };

const StatusText = ({ brew }: StatusTextProps): ReactElement => {
  if (!brew) return <>No brews yet</>;

  const { status, modified } = brew;
  if (status === "brewing") {
    return <>Currently brewing...</>;
  }

  return (
    <>
      Brewed <strong>{formatDistanceToNow(parseISO(modified)) || ""}</strong> ago
    </>
  );
};

type BrewProgressProps = { brew?: Brew };
const BrewProgress = ({ brew }: BrewProgressProps): ReactElement | null => {
  if (!brew) return null;

  const { progress, modified } = brew;
  const finishedJustNow = differenceInMinutes(new Date(), parseISO(modified)) <= 1;
  if (progress === 100 && !finishedJustNow) {
    return null;
  }
  return (
    <>
      <span className="Brew-progressbar-wrap">
        <span className="Brew-progressbar" style={{ width: `${progress}%` }} />
      </span>
      <strong>{progress}%</strong>
    </>
  );
};

type BrewerProps = { brew?: Brew };
function Brewer({ brew }: BrewerProps): ReactElement | null {
  if (!brew) return null;

  const { brewerSlackUsername } = brew;
  if (!brewerSlackUsername) return null;

  return (
    <div className="Brew-brewer">
      {/* TODO: Fetch user avatar url */}
      <img src={bg} alt={`${brewerSlackUsername}'s avatar`} className="Brew-brewer-avatar" />
      {brewerSlackUsername}
    </div>
  );
}

type BrewReactionsProps = { brew?: Brew };
function BrewReactions({ brew }: BrewReactionsProps): ReactElement | null {
  if (!brew) return null;
  const { reactions } = brew;

  return (
    <div className="Brew-reactions">
      {reactions.map((brewReaction) => {
        const { id, reaction, emoji, isCustomReaction } = brewReaction;
        return (
          <span key={id} className="Reaction-large">
            {isCustomReaction ? reaction : emoji}
          </span>
        );
      })}
    </div>
  );
}

const Machine = ({ machine }: MachineProps): ReactElement => {
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
