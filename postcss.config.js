module.exports = {
  plugins: [
    require('autoprefixer')({
      grid: true,
      browsers: ['last 2 versions', 'ie >= 11', 'iOS >= 9'],
    }),
    require('postcss-flexbugs-fixes')(),
    require('cssnano')({
      preset: 'default',
    }),
  ],
};
