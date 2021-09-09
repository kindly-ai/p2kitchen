import { gql, useQuery } from "@apollo/client";
import React, { ReactElement, useMemo } from "react";

import arrow from "../../assets/arrow.svg";
import { Machine } from "../Today/Machine";
import classes from "./Stats.module.css";

const USERS = gql`
  {
    users {
      userId
      realName
      displayName
      imageOriginal
      image48: image(size: 48)
      litersTotal
    }
  }
`;

type StatsProps = { machines: Machine[] };

export const Stats = ({ machines }: StatsProps): ReactElement => {
  const { data: dataUsers, loading } = useQuery(USERS);
  const users = useMemo(
    () => (dataUsers?.users || []).filter((user: SlackProfile) => user.litersTotal >= 1),
    [dataUsers]
  );

  if (loading) return <p>Loading...</p>;

  return (
    <section className={classes.StatsByPeriod}>
      <h2>
        This year <img src={arrow} className={classes.ArrowIcon} alt="Arrow" />
      </h2>
      <table className={classes.StatsTable}>
        <thead>
          <tr>
            <th>Machine</th>
            <th>Liter</th>
            <th>Info</th>
          </tr>
        </thead>
        <tbody>
          {machines.map((machine) => (
            <tr key={machine.id}>
              <td>
                <img
                  className={classes.StatsTableMachineAvatar}
                  src={machine.avatarUrl}
                  alt={`${machine.name}'s avatar`}
                />
                {machine.name}
              </td>
              <td>{machine.litersTotal}&nbsp;L</td>
              <td className={classes.StatsTableInfo}>{/* TODO */}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3>Colleagues brewing the most</h3>
      <table className={classes.Brewers}>
        <tbody>
          {users.map((user: SlackProfile) => (
            <tr className={classes.BrewerItem} key={user.userId}>
              <td className={classes.Brewer}>
                <img
                  className={classes.BrewerAvatar}
                  src={user.image48}
                  alt={`${user.realName || user.userId}'s avatar`}
                />
                {user.realName || user.userId}
              </td>
              <td>{user.litersTotal}&nbsp;L</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};
