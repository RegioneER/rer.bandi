import React from 'react';
import Select from 'react-select';
import { string, shape, arrayOf, func } from 'prop-types';

const SelectField = ({ parameter, value = [], updateQueryParameters }) => {
  return (
    <Select
      isMulti
      value={value.map(element => {
        return { value: element, label: element };
      })}
      name={parameter.id}
      options={parameter.options}
      onChange={options => {
        updateQueryParameters({
          [parameter.id]: options.map(option => option.value),
        });
      }}
    />
  );
};

SelectField.propTypes = {
  parameter: shape({
    id: string,
    options: arrayOf(shape({ label: string, value: string })),
  }),
  value: arrayOf(string),
  updateQueryParameters: func,
};

export default SelectField;
