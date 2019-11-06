import { LoggedInBasePage } from "./loggedInBase";
import React, { useContext, useEffect, useState } from "react";
import { SessionContext } from "./session";
import { Redirect } from "react-router-dom";
import { FieldArray, Form, Formik } from "formik";
import { Checkbox, FormControlLabel } from "@material-ui/core";

const getYouths = () => {
  return ["Test Youth 1", "Test Youth 2"];
};

const AttendanceForm = props => {
  const [youths, setYouths] = useState(getYouths());
  const onSubmit = () => {
    console.log("Submitting attendance form");
  };
  const initialValues = {
    youths: new Map(youths.map(youth => [youth, false]))
  };
  return (
    <Formik
      onSubmit={onSubmit}
      initialValues={initialValues}
      render={({ errors, isSubmitting }) => (
        <div>
          <Form>
            <FieldArray name={"friends"} render={arrayHelpers => <div><i/dv>} />
          </Form>
        </div>
      )}
    />
  );
};

const AttendancePage = () => {
  return (
    <LoggedInBasePage title="Attendance">
      <AttendanceForm />
    </LoggedInBasePage>
  );
};
export function Attendance() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => {
    console.log(`Rendering attendance page, logged in? ${loggedIn}`);
  });

  return loggedIn ? <AttendancePage /> : <Redirect to="/login" />;
}
