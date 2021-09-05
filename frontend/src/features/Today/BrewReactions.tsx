import React, { ReactElement } from "react";

type BrewReactionsProps = { brew?: Brew };

export function BrewReactions({ brew }: BrewReactionsProps): ReactElement | null {
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
