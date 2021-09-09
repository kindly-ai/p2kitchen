import { formatDistanceToNow, parseISO } from "date-fns";
import React, { ReactElement } from "react";

type StatusTextProps = { brew?: Brew };

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
