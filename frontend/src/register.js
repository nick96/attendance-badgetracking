//@flow
import React, { useState } from "react";
import { ErrorMessage, Field, Form, Formik } from "formik";
import { Link, Redirect } from "react-router-dom";
import Button from "@material-ui/core/Button";
import { TextField } from "formik-material-ui";
import { useSnackbar } from "notistack";
import * as Yup from "yup";

const RegisterFormSchema = Yup.object().shape({
  email: Yup.string()
    .email("Email is not valid")
    .required("Email is required"),
  firstName: Yup.string().required("First name is required"),
  lastName: Yup.string().required("Last name is required"),
  password: Yup.string().required("Password is required"),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref("password")], "Different to password")
    .required("Confirm password is required")
});

function RegisterForm({ onSubmit }) {
  return (
    <Formik
      initialValues={{
        email: "",
        firstName: "",
        lastName: "",
        password: "",
        confirmPassword: ""
      }}
      validationSchema={RegisterFormSchema}
      onSubmit={onSubmit}
      render={({ isSubmitting, errors }) => (
        <div>
          <Form>
            <Field
              type="email"
              name="email"
              placeholder="Email"
              variant="outlined"
              component={TextField}
              margin="normal"
            />
            <br />
            <Field
              type="text"
              name="firstName"
              placeholder="First Name"
              variant="outlined"
              component={TextField}
              margin="normal"
            />
            <br />
            <Field
              type="text"
              name="lastName"
              placeholder="Last Name"
              variant="outlined"
              component={TextField}
              margin="normal"
            />
            <br />
            <Field
              type="password"
              name="password"
              placeholder="Password"
              variant="outlined"
              component={TextField}
              margin="normal"
            />
            <br />
            <Field
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              variant="outlined"
              component={TextField}
              margin="normal"
            />
            <br />

            <React.Fragment>
              <Button
                type="submit"
                disabled={isSubmitting}
                variant="contained"
                margin="normal"
                fullWidth
                color="primary"
              >
                Submit
              </Button>
              <div style={{ color: "red" }}>{errors.general}</div>
            </React.Fragment>
          </Form>
          <Link
            to="/login"
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center"
            }}
          >
            Sign in
          </Link>
        </div>
      )}
    />
  );
}

export function Register({ client }) {
  const { enqueueSnackbar } = useSnackbar();
  const [registered, setRegistered] = useState(0);
  const onSubmit = (values, { setSubmitting, setErrors }) => {
    setTimeout(() => {
      client
        .registerUser({
          email: values.email,
          firstName: values.firstName,
          lastName: values.lastName,
          password: values.password
        })
        .then(user => {
          setRegistered(true);
          enqueueSnackbar("Registration successful", {
            variant: "success",
            anchorOrigin: {
              vertical: "top",
              horizontal: "center"
            }
          });
        })
        .catch(err => setErrors({ general: err.message }))
        .finally(() => setSubmitting(false));
    }, 400);
  };
  return registered ? (
    <Redirect to="/login" />
  ) : (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <RegisterForm onSubmit={onSubmit} />
    </div>
  );
}
