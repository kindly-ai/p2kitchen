import React, { ReactElement } from "react";

import StatsByPeriod from "./StatsByPeriod";
import bg from "./assets/bg.jpg";
import "./App.css";

const App = (): ReactElement => {
  const MachineBrewProgress = 71;
  return (
    <div className="App">
      <main className="App-container">
        <div className="Panel">
          <section className="Status">
            <h2>Today & now</h2>
            <p>Where to find the freshest coffee right now</p>
            <div className="Machine-item">
              <img src={bg} className="Machine-avatar" alt="Machine avatar" />
              <div className="Brew">
                <h3>Bryggvar den store</h3>
                <div className="Brew-status">Currently brewing....</div>
                <div>
                  <span className="Brew-progressbar" style={{ width: `${MachineBrewProgress}px` }} />
                  <strong>{MachineBrewProgress}%</strong>
                </div>
              </div>
            </div>
            <div className="Machine-item">
              <img src={bg} className="Machine-avatar" alt="Machine avatar" />
              <div className="Brew">
                <h3>Grutenberg</h3>
                <div className="Brew-status">
                  Brewed <strong>7 minutes</strong> ago
                </div>
                <div className="Brew-brewer">
                  <img src={bg} alt="Nikolai's avatar" className="Brew-brewer-avatar" />
                  Nikolai Kristiansen
                </div>
              </div>
              <div className="Brew-reactions">
                <span className="Reaction-large">👏</span>
                <span className="Reaction-small">👌</span>
                <span className="Reaction-small">🤠</span>
                <span className="Reaction-small">❤️</span>
              </div>
            </div>
            <p className="Summary">
              Your team has brewed & consumed 13,5l coffee today, 4l less than yesterday. Keep drinking!!
            </p>
          </section>
          <StatsByPeriod />
        </div>
      </main>
    </div>
  );
};

export default App;
