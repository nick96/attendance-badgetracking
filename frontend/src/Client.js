//@flow

import * as request from "superagent";
import { createContext } from "react";

export type RegisterUser = {
  email: string,
  firstName: string,
  lastName: string,
  email: string,
  password: string
};

export type User = {
  id: number,
  email: string,
  firstName: string,
  lastName: string
};

export type Credentials = {
  email: string,
  password: string
};

function handleError(err) {
  if (err.response.body.error) {
    throw new Error(err.response.body.error);
  }
  throw new Error(err.message);
}

export class Client {
  baseUrl: string;
  token: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  registerUser(body: RegisterUser): Promise<User, Error> {
    return request
      .post(`${this.baseUrl}/user`)
      .send(body)
      .then(resp => new Promise(resolve => resolve(User(resp.body))))
      .catch(handleError);
  }

  loginUser(body: Credentials): Promise<string, Error> {
    return request
      .post(`${this.baseUrl}/login`)
      .send(body)
      .then(resp => {
        this.token = resp.body.token;
        return new Promise(resolve => resolve(resp.body.token));
      })
      .catch(handleError);
  }
}

export const ClientContext = createContext();
