import React from 'react';
import { array, string, object, oneOfType, func } from 'prop-types';
import TextField from '../fields/TextField';
import SelectField from '../fields/SelectField';
import CheckboxField from '../fields/CheckboxField';

const FormFieldWrapper = ({ parameter, value, updateQueryParameters }) => {
  let FieldComponent = '';

  switch (parameter.type) {
    case 'select':
      FieldComponent = SelectField;
      break;
    case 'checkbox':
      FieldComponent = CheckboxField;
      break;
    default:
      FieldComponent = TextField;
  }

  return (
    <div className="field">
      <label>
        {parameter.label}
        <FieldComponent
          parameter={parameter}
          value={value}
          updateQueryParameters={updateQueryParameters}
        />
      </label>
    </div>
  );
};

FormFieldWrapper.propTypes = {
  parameter: object,
  updateQueryParameters: func,
  value: oneOfType([string, array]),
};

export default FormFieldWrapper;
