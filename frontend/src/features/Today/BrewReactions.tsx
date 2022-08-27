import React from "react";

type BrewReactionsProps = { brew?: MachinesQuery["machines"][0]["lastBrew"] };

import { MachinesQuery } from "../../generated";
import classes from "./Today.module.css";

export function BrewReactions({ brew }: BrewReactionsProps) {
  if (!brew) return null;
  const { reactions } = brew;

  return (
    <div className={classes.BrewReactions}>
      {reactions.map((brewReaction) => {
        const { id, reaction, emoji, isCustomReaction } = brewReaction;
        return (
          <span key={id}>
            {isCustomReaction && <img src={emoji} alt={reaction} width={21} height={21} title={reaction} />}
            {!isCustomReaction && <span title={reaction}>{emoji}</span>}
          </span>
        );
      })}
    </div>
  );
}
