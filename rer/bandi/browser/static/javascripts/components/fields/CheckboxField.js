import React from 'react';
import { string, shape, arrayOf, func } from 'prop-types';
import './CheckboxField.less';

const CheckboxField = ({ parameter, value = [], updateQueryParameters }) => {
  const updateCheckboxValue = evt => {
    const { target } = evt;
    if (!value) {
      if (target.checked) {
        updateQueryParameters({
          [parameter.id]: [target.value],
        });
        return;
      } else {
        return;
      }
    }
    if (target.checked && value.indexOf(target.value) === -1) {
      updateQueryParameters({
        [parameter.id]: [...value, target.value],
      });
    } else if (!target.checked && value.indexOf(target.value) !== -1) {
      value.splice(value.indexOf(target.value), 1);
      updateQueryParameters({
        [parameter.id]: value,
      });
    }
  };
  return (
    <fieldset>
      <legend>{parameter.label}</legend>
      {parameter.options.map(option => (
        <div className="checkbox-option" key={option.label}>
          <label>
            <input
              name={option.label}
              value={option.value}
              checked={value.includes(option.value)}
              type="checkbox"
              onChange={updateCheckboxValue}
            />
            {option.label}
          </label>
        </div>
      ))}
    </fieldset>
  );
};
CheckboxField.propTypes = {
  parameter: shape({
    id: string,
    options: arrayOf(shape({ label: string, value: string })),
  }),
  value: arrayOf(string),
  updateQueryParameters: func,
};

export default CheckboxField;
