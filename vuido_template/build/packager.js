const packager = require('launchui-packager');

packager( {
  name: 'MyApp',
  version: '1.0.0',
  entry: './dist/main.js',
  out: './packages'
}, function ( err, outPath ) {
  // outPath will be the path of the created package directory or file
} );