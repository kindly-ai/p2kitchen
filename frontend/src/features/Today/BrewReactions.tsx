import React, { ReactElement } from "react";

type BrewReactionsProps = { brew?: Brew };

import classes from "./Today.module.css";

export function BrewReactions({ brew }: BrewReactionsProps): ReactElement | null {
  if (!brew) return null;
  const { reactions } = brew;

  return (
    <div className={classes.BrewReactions}>
      {reactions.map((brewReaction) => {
        const { id, reaction, emoji, isCustomReaction } = brewReaction;
        return <span key={id}>{isCustomReaction ? reaction : emoji}</span>;
      })}
    </div>
  );
}
