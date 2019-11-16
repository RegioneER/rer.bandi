import React, { useState, useEffect } from 'react';
import { array } from 'prop-types';
import axios from 'axios';

export const TranslationsContext = React.createContext({});

export const TranslationsProvider = TranslationsContext.Provider;
export const TranslationsConsumer = TranslationsContext.Consumer;

function TranslationsWrapper({ children }) {
  const [translations, setTranslations] = useState({});

  useEffect(() => {
    const catalogUrl = document
      .querySelector('body')
      .getAttribute('data-i18ncatalogurl');
    if (!catalogUrl) {
      return;
    }
    let language = document.querySelector('html').getAttribute('lang');
    if (!language) {
      language = 'en';
    }
    const domain = 'rer.bandi';
    axios({
      method: 'GET',
      url: catalogUrl,
      params: { domain, language },
    })
      .then(({ data }) => {
        setTranslations({ ...data, language });
      })
      .catch(function(error) {
        // handle error
        console.log(error);
      });
  }, []);

  const getTranslationFor = (msgid, defaultMsg, value = '') => {
    if (!translations[msgid]) {
      return defaultMsg;
    }
    return translations[msgid].replace(/(\${variable})/g, value);
  };

  return (
    <TranslationsProvider value={getTranslationFor}>
      {children}
    </TranslationsProvider>
  );
}

TranslationsWrapper.propTypes = {
  children: array,
};

export default TranslationsWrapper;
