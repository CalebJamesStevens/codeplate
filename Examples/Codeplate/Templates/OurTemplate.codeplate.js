import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

/** MaterialUI Components */
import Box from '@mui/material/Box';

/** Components */

/** styles */
import styles from './codeplate_componentName.styles';

/** actions */

/** helpers */

export const codeplate_componentName = () => {


  return (
    <Box sx={styles.codeplate_styleName}/>
  );
};

codeplate_componentName.propTypes = {

};

/* istanbul ignore next */
export default connect(
  state => ({
    state
  }),
  {
  }
)(codeplate_componentName);
