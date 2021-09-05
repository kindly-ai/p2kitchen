import React, { ReactElement } from "react";

import bg from "../../assets/bg.jpg";
import slack_icon from "../../assets/slack_mark.svg";
import classes from "./Today.module.css";

type BrewerProps = { brew?: Brew };

export const Brewer = ({ brew }: BrewerProps): ReactElement | null => {
  if (!brew) return null;

  const { brewerSlackUsername } = brew;
  if (!brewerSlackUsername)
    return (
      <div className={classes.BrewBrewer}>
        <img src={slack_icon} alt="Slack Mark" className={classes.slackIcon} />
        <em>Add brewer in Slack</em>
      </div>
    );

  return (
    <div className={classes.BrewBrewer}>
      {/* TODO: Fetch user avatar url */}
      <img src={bg} alt={`${brewerSlackUsername}'s avatar`} className={classes.BrewBrewerAvatar} />
      {brewerSlackUsername}
    </div>
  );
};
