import { LoggedInBasePage } from "./loggedInBase";
import React, { useContext, useEffect } from "react";
import { SessionContext } from "./session";
import { Redirect } from "react-router-dom";

const SettingsPage = () => (
  <LoggedInBasePage title="Home">Home</LoggedInBasePage>
);

export function Settings() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => {
    console.log(`Rendering settings page, logged in? ${loggedIn}`);
  });

  return loggedIn ? <SettingsPage /> : <Redirect to="/login" />;
}
