import { differenceInMinutes, parseISO } from "date-fns";
import React, { ReactElement } from "react";

import classes from "./Today.module.css";

type BrewProgressProps = { brew?: Brew };

export const BrewProgress = ({ brew }: BrewProgressProps): ReactElement | null => {
  if (!brew) return null;

  const { progress, modified } = brew;
  const finishedJustNow = differenceInMinutes(new Date(), parseISO(modified)) <= 1;
  if (progress === 100 && !finishedJustNow) {
    return null;
  }
  return (
    <>
      <span className={classes.BrewProgressbarWrap}>
        <span className={classes.BrewProgressbar} style={{ width: `${progress}%` }} />
      </span>
      <strong>{progress}%</strong>
    </>
  );
};
