import { LoggedInBasePage } from "./loggedInBase";
import React, { useContext, useEffect } from "react";
import { SessionContext } from "./session";
import { Redirect } from "react-router-dom";

const GroupsPage = () => <LoggedInBasePage title="Home">Home</LoggedInBasePage>;

export function Groups() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => {
    console.log(`Rendering Groups page, logged in? ${loggedIn}`);
  });

  return loggedIn ? <GroupsPage /> : <Redirect to="/login" />;
}
