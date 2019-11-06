import { LoggedInBasePage } from "./loggedInBase";
import React, { useContext, useEffect } from "react";
import { SessionContext } from "./session";
import { Redirect } from "react-router-dom";

const BadgetrackingPage = () => (
  <LoggedInBasePage title="Home">Home</LoggedInBasePage>
);

export function Badgetracking() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => {
    console.log(`Rendering Badgetracking page, logged in? ${loggedIn}`);
  });

  return loggedIn ? <BadgetrackingPage /> : <Redirect to="/login" />;
}
