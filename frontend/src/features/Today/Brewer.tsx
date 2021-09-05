import React, { ReactElement } from "react";

import bg from "../../assets/bg.jpg";
import slack_icon from "../../assets/slack_mark.svg";
import classes from "./Today.module.css";

type BrewerProps = { brew?: Brew };

export const Brewer = ({ brew }: BrewerProps): ReactElement | null => {
  if (!brew) return null;

  const { brewer } = brew;
  if (!brewer)
    return (
      <div className={classes.BrewBrewer}>
        <img src={slack_icon} alt="Slack Mark" className={classes.slackIcon} />
        <em>Add brewer in Slack</em>
      </div>
    );

  return (
    <div className={classes.BrewBrewer}>
      <img
        src={brewer.image48 || bg}
        alt={`${brewer.realName || brewer.userId}'s avatar`}
        className={classes.BrewBrewerAvatar}
      />
      {brewer.realName || brewer.userId}
    </div>
  );
};
