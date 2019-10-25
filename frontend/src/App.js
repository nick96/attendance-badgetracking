import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Login } from "./login";
import { Home } from "./home";
import { Register } from "./register";
import { Client, ClientContext } from "./Client";
import { SessionContextProvider } from "./session";

const AppRouter = () => (
  <Router>
    <Switch>
      <Route path="/register" component={props => <Register {...props} />} />
      <Route path="/login" component={props => <Login {...props} />} />
      <Route path="/" component={props => <Home {...props} />} />
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
