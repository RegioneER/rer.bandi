import React, { useContext } from 'react';
import Select from 'react-select';
import { string, shape, arrayOf, func, bool } from 'prop-types';
import { TranslationsContext } from '../../TranslationsContext';

const SelectField = ({ parameter, value = [], updateQueryParameters }) => {
  const getTranslationFor = useContext(TranslationsContext);
  return (
    <React.Fragment>
      <label htmlFor={parameter.id}>{parameter.label}</label>
      {parameter.help.length ? (
        <p className="discreet">{parameter.help}</p>
      ) : (
        ''
      )}
      <Select
        isMulti={parameter.multivalued}
        inputId={parameter.id}
        tabSelectsValue={false}
        value={value.map(element => {
          return {
            value: element,
            label:
              element !== ''
                ? getTranslationFor(
                    `bando_state_${element}_select_label`,
                    element,
                  )
                : getTranslationFor('bando_state_all_select_label', element),
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
    </React.Fragment>
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
