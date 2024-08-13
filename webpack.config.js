const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: './01_application/webcentral_app/webcentral_app/static/css/webcentral.scss',
  output: {
    path: path.resolve(__dirname, '01_application/webcentral_app/webcentral_app/static/webpack_bundles/'),
    filename: '[name].js', // Not used for CSS but required by Webpack
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'webcentral.[contenthash].css',
    }),
    new BundleTracker({ path: `${__dirname}/01_application/webcentral_app/`, filename: 'webpack-stats.json' })
  ],
};
