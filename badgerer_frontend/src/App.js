import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Login } from "./login";
import { Home } from "./home";
import { Register } from "./register";
import { Client, ClientContext } from "./Client";
import { SessionContextProvider } from "./session";
import { Attendance } from "./attendance";
import { Badgetracking } from "./badgetracking";
import { Groups } from "./groups";
import { Plans } from "./plans";
import { Settings } from "./settings";

const AppRouter = () => (
  <Router>
    <Switch>
      <Route path="/register" component={props => <Register {...props} />} />
      <Route path="/login" component={props => <Login {...props} />} />
      <Route path="/(home)?" exact component={props => <Home {...props} />} />
      <Route
        path="/attendance"
        exact
        component={props => <Attendance {...props} />}
      />
      <Route
        path="/badgetracking"
        exact
        component={props => <Badgetracking {...props} />}
      />
      <Route path="/groups" exact component={props => <Groups {...props} />} />
      <Route path="/plans" exact component={props => <Plans {...props} />} />
      <Route
        path="/settings"
        exact
        component={props => <Settings {...props} />}
      />
    </Switch>
  </Router>
);

export default function App() {
  const client = new Client(
    process.env.REACT_APP_API_URL || "http://localhost:5000"
  );

  return (
    <SessionContextProvider>
      <ClientContext.Provider value={client}>
        <AppRouter />
      </ClientContext.Provider>
    </SessionContextProvider>
  );
}
