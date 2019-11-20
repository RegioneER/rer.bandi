import React, { useContext } from 'react';
import Select from 'react-select';
import { string, shape, arrayOf, func } from 'prop-types';
import { TranslationsContext } from '../../TranslationsContext';

const SelectField = ({ parameter, value = [], updateQueryParameters }) => {
  const getTranslationFor = useContext(TranslationsContext);

  return (
    <Select
      isMulti
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
        updateQueryParameters({
          [parameter.id]: options ? options.map(option => option.value) : [],
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
