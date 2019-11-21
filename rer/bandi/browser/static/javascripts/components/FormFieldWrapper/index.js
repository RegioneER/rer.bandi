import React from 'react';
import { array, string, object, oneOfType, func } from 'prop-types';
import TextField from '../fields/TextField';
import SelectField from '../fields/SelectField';
import CheckboxField from '../fields/CheckboxField';

import './index.less';

const FormFieldWrapper = ({ parameter, value, updateQueryParameters }) => {
  let FieldComponent = '';
  let className = '';

  switch (parameter.type) {
    case 'select':
      FieldComponent = SelectField;
      className = 'select';
      break;
    case 'checkbox':
      FieldComponent = CheckboxField;
      className = 'checkbox';
      break;
    default:
      FieldComponent = TextField;
      className = 'text';
  }

  return (
    <div className={`field ${className}-field`}>
      <label>
        <span>{parameter.label}</span>
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
