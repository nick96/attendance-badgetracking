import { LoggedInBasePage } from "./loggedInBase";
import React, { useContext, useEffect } from "react";
import { SessionContext } from "./session";
import { Redirect } from "react-router-dom";

const LibrariesPage = () => (
  <LoggedInBasePage title="Home">Home</LoggedInBasePage>
);

export function Libraries() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => {
    console.log(`Rendering Libraries page, logged in? ${loggedIn}`);
  });

  return loggedIn ? <LibrariesPage /> : <Redi1rect to="/login" />;
}
