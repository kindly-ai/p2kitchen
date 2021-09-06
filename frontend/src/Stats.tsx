import { gql, useQuery } from "@apollo/client";
import React, { ReactElement, useMemo } from "react";

import arrow from "./assets/arrow.svg";
import "./Stats.css";
import { Machine } from "./features/Today/Machine";

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

const Stats = ({ machines }: StatsProps): ReactElement => {
  const { data: dataUsers, loading } = useQuery(USERS);
  const users = useMemo(
    () => (dataUsers?.users || []).filter((user: SlackProfile) => user.litersTotal >= 1),
    [dataUsers]
  );

  if (loading) return <p>Loading...</p>;

  return (
    <section className="StatsByPeriod">
      <h2>
        This year <img src={arrow} className="Arrow-icon" alt="Arrow" />
      </h2>
      <table className="StatsTable">
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
                <img className="StatsTable-machine-avatar" src={machine.avatarUrl} alt={`${machine.name}'s avatar`} />
                {machine.name}
              </td>
              <td>{machine.litersTotal}&nbsp;L</td>
              <td className="StatsTable-info">{/* TODO */}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3>Colleagues brewing the most</h3>
      <table className="Brewers">
        <tbody>
          {/*TODO: unclaimed brews */}
          {/*<tr className="BrewerItem">*/}
          {/*  <td className="Brewer">*/}
          {/*    <img className="Brewer-avatar" src={bg} alt="Unknown's avatar" />*/}
          {/*    Unknown*/}
          {/*  </td>*/}
          {/*  <td>143&nbsp;L</td>*/}
          {/*</tr>*/}
          {users.map((user: SlackProfile) => (
            <tr className="BrewerItem" key={user.userId}>
              <td className="Brewer">
                <img className="Brewer-avatar" src={user.image48} alt={`${user.realName || user.userId}'s avatar`} />
                {user.realName || user.userId}
              </td>
              <td className="Brewer">{user.litersTotal}&nbsp;L</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};

export default Stats;
