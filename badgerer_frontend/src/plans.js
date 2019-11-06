import { LoggedInBasePage } from "./loggedInBase";
import React, { useContext, useEffect } from "react";
import { SessionContext } from "./session";
import { Redirect } from "react-router-dom";

const PlansPage = () => <LoggedInBasePage title="Home">Home</LoggedInBasePage>;

export function Plans() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => {
    console.log(`Rendering Plans page, logged in? ${loggedIn}`);
  });

  return loggedIn ? <PlansPage /> : <Redirect to="/login" />;
}
