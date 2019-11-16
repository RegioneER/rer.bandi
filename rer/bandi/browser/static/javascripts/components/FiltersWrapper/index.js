import React, { useContext } from 'react';
import { array, bool, object, func } from 'prop-types';
import FormFieldWrapper from '../FormFieldWrapper';
import { TranslationsContext } from '../../TranslationsContext';

const FiltersWrapper = ({
  formParameters,
  queryParameters,
  isFetching,
  updateQueryParameters,
}) => {
  const getTranslationFor = useContext(TranslationsContext);

  if (isFetching) {
    return <div>isFetching</div>;
  }
  return (
    <div className="search-filter">
      <h2 className="refineSearch">
        {getTranslationFor('refine_search_label', 'Refine your search')}
      </h2>
      {formParameters && formParameters.length
        ? formParameters.map(parameter => (
            <FormFieldWrapper
              parameter={parameter}
              key={parameter.id}
              value={queryParameters[parameter.id]}
              updateQueryParameters={updateQueryParameters}
            />
          ))
        : ''}
    </div>
  );
};
FiltersWrapper.propTypes = {
  formParameters: array,
  queryParameters: object,
  isFetching: bool,
  updateQueryParameters: func,
};

export default FiltersWrapper;
