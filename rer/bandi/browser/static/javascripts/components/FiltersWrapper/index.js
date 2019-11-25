import React, { useContext } from 'react';
import { array, bool, object, func } from 'prop-types';
import FormFieldWrapper from '../FormFieldWrapper';
import { TranslationsContext } from '../../TranslationsContext';

import './index.less';

const FiltersWrapper = ({
  formParameters,
  queryParameters,
  isFetching,
  updateQueryParameters,
  resetQueryParameters,
}) => {
  const getTranslationFor = useContext(TranslationsContext);

  const filtersContent = isFetching ? (
    <div>Loading...</div>
  ) : (
    <React.Fragment>
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
      <div className="reset-filters">
        <button onClick={resetQueryParameters} className="btn btn-secondary">
          {getTranslationFor('reset_filters_label', 'Reset all filters')}
        </button>
      </div>
    </React.Fragment>
  );

  return (
    <div className="search-filter col-lg-4 col-md-6 col-sm-12">
      {filtersContent}
    </div>
  );
};
FiltersWrapper.propTypes = {
  formParameters: array,
  queryParameters: object,
  isFetching: bool,
  updateQueryParameters: func,
  resetQueryParameters: func,
};

export default FiltersWrapper;
