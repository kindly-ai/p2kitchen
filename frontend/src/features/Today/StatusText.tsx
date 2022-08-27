import { formatDistanceToNow, parseISO } from "date-fns";
import React, { ReactElement } from "react";

import { MachinesQuery } from "../../generated";

type StatusTextProps = { brew?: MachinesQuery["machines"][0]["lastBrew"] };

export const StatusText = ({ brew }: StatusTextProps): ReactElement => {
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
