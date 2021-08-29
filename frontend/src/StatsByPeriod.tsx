import React, { ReactElement } from "react";

import arrow from "./assets/arrow.svg";
import bg from "./assets/bg.jpg";

import "./StatsByPeriod.css";

const StatsByPeriod = (): ReactElement => (
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
          <td>420 L</td>
          <td className="StatsTable-info">Need descaling</td>
        </tr>
        <tr>
          <td>
            <img className="StatsTable-machine-avatar" src={bg} alt="Grutenberg's avatar" />
            Grutenberg
          </td>
          <td>241 L</td>
          <td className="StatsTable-info" />
        </tr>
        <tr>
          <td>
            <img className="StatsTable-machine-avatar" src={bg} alt="Kaffelars's avatar" />
            Kaffelars
          </td>
          <td>69 L</td>
          <td className="StatsTable-info">Need descaling</td>
        </tr>
      </tbody>
    </table>
    <h3>Colleagues breewing the most</h3>
    <table className="Brewers">
      <tbody>
        <tr className="BrewerItem">
          <td className="Brewer">
            <img className="Brewer-avatar" src={bg} alt="Unknown's avatar" />
            Unknown person with an insane name
          </td>
          <td>143 L</td>
        </tr>
        <tr className="BrewerItem">
          <td className="Brewer">
            <img className="Brewer-avatar" src={bg} alt="Nikolai's avatar" />
            Nikolai Kristiansen
          </td>
          <td className="Brewer">42 L</td>
        </tr>
      </tbody>
    </table>
  </section>
);

export default StatsByPeriod;
