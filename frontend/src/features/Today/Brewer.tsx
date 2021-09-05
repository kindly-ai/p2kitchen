import React, { ReactElement } from "react";

import bg from "../../assets/bg.jpg";

type BrewerProps = { brew?: Brew };

export const Brewer = ({ brew }: BrewerProps): ReactElement | null => {
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
};
