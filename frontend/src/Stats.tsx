import { gql, useQuery } from "@apollo/client";
import React, { ReactElement, useMemo } from "react";

import arrow from "./assets/arrow.svg";
import bg from "./assets/bg.jpg";

import "./Stats.css";

const TOP_USERS = gql`
  {
    topUsers {
      userId
      realName
      displayName
      imageOriginal
      image48: image(size: 48)
      litersTotal
    }
  }
`;
const Stats = (): ReactElement => {
  const { data: dataTopUsers, loading } = useQuery(TOP_USERS);
  const topUsers = useMemo(
    () => (dataTopUsers?.topUsers || []).filter((topUser: TopUser) => topUser.litersTotal >= 1),
    [dataTopUsers]
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
          <tr>
            <td>
              <img className="StatsTable-machine-avatar" src={bg} alt="Bryggvar's avatar" />
              Bryggvar
            </td>
            <td>420&nbsp;L</td>
            <td className="StatsTable-info">Need descaling</td>
          </tr>
          <tr>
            <td>
              <img className="StatsTable-machine-avatar" src={bg} alt="Grutenberg's avatar" />
              Grutenberg
            </td>
            <td>241&nbsp;L</td>
            <td className="StatsTable-info" />
          </tr>
          <tr>
            <td>
              <img className="StatsTable-machine-avatar" src={bg} alt="Kaffelars's avatar" />
              Kaffelars
            </td>
            <td>69&nbsp;L</td>
            <td className="StatsTable-info">Need descaling</td>
          </tr>
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
          {topUsers.map((topUser: TopUser) => (
            <tr className="BrewerItem" key={topUser.userId}>
              <td className="Brewer">
                <img
                  className="Brewer-avatar"
                  src={topUser.image48}
                  alt={`${topUser.realName || topUser.userId}'s avatar`}
                />
                {topUser.realName || topUser.userId}
              </td>
              <td className="Brewer">{topUser.litersTotal}&nbsp;L</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};

export default Stats;
