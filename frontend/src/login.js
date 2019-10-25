import { ErrorMessage, Field, Form, Formik } from "formik";
import React, { useContext, useEffect } from "react";
import { Link, Redirect } from "react-router-dom";
import { TextField } from "formik-material-ui";

import Button from "@material-ui/core/Button";
import type { Credentials } from "./Client";
import * as Yup from "yup";
import { SessionContext } from "./session";
import { ClientContext } from "./Client";

const LoginFormSchema = Yup.object().shape({
  email: Yup.string()
    .email("Email is not valid")
    .required("Email is required"),
  password: Yup.string().required("Password is required")
});

function LoginForm({ onSubmit }) {
  return (
    <Formik
      initialValues={{ email: "", password: "" }}
      validationSchema={LoginFormSchema}
      onSubmit={onSubmit}
      render={props => (
        <div>
          <Form>
            <Field
              type="email"
              name="email"
              placeholder="Email"
              component={TextField}
              variant="outlined"
              margin="normal"
              fullWidth
            />
            <br />
            <Field
              type="password"
              name="password"
              placeholder="Password"
              component={TextField}
              variant="outlined"
              margin="normal"
              fullWidth
            />
            <br />
            <React.Fragment>
              <Button
                type="submit"
                disabled={props.isSubmitting}
                variant="contained"
                margin="normal"
                color="primary"
                fullWidth
              >
                Submit
              </Button>
              <div style={{ color: "red" }}>{props.errors.general}</div>
            </React.Fragment>
          </Form>
          <Link
            to="/register"
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center"
            }}
          >
            Sign up
          </Link>
        </div>
      )}
    />
  );
}

const LoginPage = () => {
  const { setSession } = useContext(SessionContext);
  const client = useContext(ClientContext);

  const onSubmit = (values, { setSubmitting, setErrors }) => {
    setTimeout(() => {
      client
        .loginUser((values: Credentials))
        .then(token => {
          console.log(`Setting session to returned token ${token}`);
          setSession(token);
        })
        .catch(err => {
          console.error(`Could not login user: ${err}`);
          setErrors({ general: err.message });
        })
        .finally(() => setSubmitting(false));
    }, 400);
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <LoginForm onSubmit={onSubmit} />
    </div>
  );
};

export function Login() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => console.log(`Rendering login page, logged in? ${loggedIn}`));
  return !loggedIn ? <LoginPage /> : <Redirect to="/" />;
}
