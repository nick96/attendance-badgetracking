import React, { useContext, useEffect } from "react";
import { Redirect } from "react-router-dom";
import { SessionContext } from "./session";
import { LoggedInBasePage } from "./loggedInBase";

const HomePage = () => <LoggedInBasePage title="Home">Home</LoggedInBasePage>;

export function Home() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => {
    console.log(`Rendering home page, logged in? ${loggedIn}`);
  });

  return loggedIn ? <HomePage /> : <Redirect to="/login" />;
}
