import React, { useContext } from 'react';
import { object } from 'prop-types';
import { format, isPast } from 'date-fns';
import { TranslationsContext } from '../../TranslationsContext';

import './index.less';

const BandoItem = ({ data }) => {
  const getTranslationFor = useContext(TranslationsContext);
  const calculateState = ({
    getScadenza_bando,
    getChiusura_procedimento_bando,
  }) => {
    let state = 'open';
    const scadenzaDate = getScadenza_bando.length
      ? new Date(getScadenza_bando)
      : null;
    const chiusuraDate = getChiusura_procedimento_bando.length
      ? new Date(getChiusura_procedimento_bando)
      : null;
    if (scadenzaDate && isPast(scadenzaDate)) {
      if (isPast(chiusuraDate)) {
        state = 'closed';
      } else {
        state = 'inProgress';
      }
    } else {
      if (isPast(chiusuraDate)) {
        state = 'closed';
      }
    }
    return state;
  };

  const { effective, getScadenza_bando } = data;
  const bandoState = calculateState(data);
  const effectiveDate = effective ? (
    <p>
      {getTranslationFor('bandi_published_on', '')}
      :&nbsp;
      {format(new Date(effective), 'dd/MM/yyyy')}
    </p>
  ) : (
    ''
  );
  const scadenzaBando = getScadenza_bando ? (
    <p>
      {getTranslationFor('bando_scadenza_partecipazione', '')}
      :&nbsp;
      {format(new Date(getScadenza_bando), 'dd/MM/yyyy HH:mm')}
    </p>
  ) : (
    ''
  );
  return (
    <div className="bando-result">
      <h3 className="bandoTitle contenttype-bando">
        <span className={`state-${bandoState} bandoStateClass`}>
          {getTranslationFor(
            `bandi_search_state_${bandoState.toLowerCase()}`,
            bandoState,
          )}
        </span>
        <a className={`state-${data.review_state}`} href={data['@id']}>
          <span>{data.title}</span>
        </a>
      </h3>
      <div className="bandoDetail">
        {data.description}
        <div className="bandoDates">
          {effectiveDate}
          {effectiveDate && scadenzaBando ? (
            <span className="separator">|</span>
          ) : (
            ''
          )}
          {scadenzaBando}
        </div>
      </div>
    </div>
  );
};

BandoItem.propTypes = {
  data: object,
};

export default BandoItem;
