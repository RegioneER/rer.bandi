import React, { useContext } from 'react';
import Select from 'react-select';
import { string, shape, arrayOf, func, bool } from 'prop-types';
import { TranslationsContext } from '../../TranslationsContext';

const SelectField = ({ parameter, value = [], updateQueryParameters }) => {
  const getTranslationFor = useContext(TranslationsContext);
  console.log(value);
  return (
    <Select
      isMulti={parameter.multivalued}
      value={value.map(element => {
        return {
          value: element,
          label:
            element !== ''
              ? getTranslationFor(element, element)
              : getTranslationFor('bandi_search_state_all', element),
        };
      })}
      name={parameter.id}
      options={parameter.options}
      placeholder={getTranslationFor('select_placeholder', 'Select...')}
      onChange={options => {
        let newValue = [];
        if (options) {
          newValue = parameter.multivalued
            ? options.map(option => option.value)
            : [options.value];
        }
        updateQueryParameters({
          [parameter.id]: newValue,
        });
      }}
    />
  );
};

SelectField.propTypes = {
  parameter: shape({
    id: string,
    options: arrayOf(shape({ label: string, value: string })),
    multivalued: bool,
  }),
  value: arrayOf(string),
  updateQueryParameters: func,
};

export default SelectField;
