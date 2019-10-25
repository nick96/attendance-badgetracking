//@flow
import Cookies from "js-cookie";
import React, { createContext, useReducer } from "react";

export const SessionContext = createContext();

const parseJWT = (token: string) => {
  if (token) {
    console.log(`Decoding token ${token}`);
    const base64Url = token.split(".")[1];
    console.log(`Base 64 URL ${base64Url}`);
    const base64 = base64Url.replace("-", "+").replace("_", "/");
    console.log(`Base 64 ${base64Url}`);
    return JSON.parse(window.atob(base64));
  }
};

const getSession = (): ?string => {
  console.log("Getting session");
  const jwt = Cookies.get("__session");
  if (jwt) {
    console.log(`Found session ${jwt}`);
    return new Session(jwt);
  }
  console.log("No session was found");
  return null;
};

export class Session {
  token: string;
  firstName: string;
  lastName: string;
  email: string;

  constructor(token: string) {
    this.token = token;
    const parsedToken = parseJWT(token);
    if (parsedToken) {
      this.firstName = parsedToken.fnm;
      this.lastName = parsedToken.lnm;
      this.email = parsedToken.sub;
    }
  }
}

const initialState = {
  session: getSession(),
  loggedIn: !!getSession()
};

const reducer = (state = initialState, action) => {
  console.log(
    `Calling reducer for action ${
      action.type
    }, current state is ${JSON.stringify(state)}`
  );
  switch (action.type) {
    case "setSession":
      Cookies.set("__session", action.payload);
      return { ...state, loggedIn: true, session: getSession() };
    case "clearSession":
      Cookies.remove("__session");
      return { ...state, loggedIn: false, session: null };
    default:
      console.warn(`Action ${action.type} not handled`);
      return state;
  }
};
export const SessionContextProvider = props => {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <SessionContext.Provider
      value={{
        ...state,
        setSession: session =>
          dispatch({ type: "setSession", payload: session }),
        clearSession: () => dispatch({ type: "clearSession" })
      }}
    >
      {props.children}
    </SessionContext.Provider>
  );
};
