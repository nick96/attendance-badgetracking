import React from "react";
import { Redirect, Route } from "react-router-dom";
import { SessionContext } from "./session";

export function PrivateRoute({ component: Component, ...rest }) {
  return (
    <SessionContext.Consumer>
      {({ session }) => (
        <Route
          {...rest}
          render={props =>
            session ? (
              <Component {...props} />
            ) : (
              <Redirect
                to={{
                  pathname: "/login",
                  state: { from: props.location }
                }}
              />
            )
          }
        />
      )}
    </SessionContext.Consumer>
  );
}
